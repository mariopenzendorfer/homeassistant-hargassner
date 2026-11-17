"""Exercise TCP message framing through the real receiver and parser."""

import asyncio
from types import SimpleNamespace

import pytest

from conftest import load_module

HargassnerTelnetClient = load_module("telnet_client").HargassnerTelnetClient


def temperature_message(client, temperature):
    """Build a full wire message with a recognizable temperature."""
    values = ["0"] * client.expected_message_length
    values[client._parser.get_parameter_info("TK").index] = str(temperature)
    return ("pm " + " ".join(values) + "\r\n").encode()


async def receive_chunks(client, chunks):
    """Simulate deterministic TCP reads and timeouts, then close at EOF."""
    pending = iter(chunks)

    async def read(size):
        chunk = next(pending, None)
        if chunk is None:
            client._running = False
            return b""
        if isinstance(chunk, Exception):
            raise chunk
        return chunk

    client._reader = SimpleNamespace(read=read)
    client._connected = client._running = True
    await asyncio.wait_for(client._receiver_loop(), timeout=2)


@pytest.mark.parametrize("firmware", ["V14_1HAR_q1", "V10_2HAR_n2"])
@pytest.mark.parametrize("split_at", ["prefix", "number", "newline", "every_byte"])
def test_fragmented_message_publishes_only_complete_values(firmware, split_at):
    """No callback may expose a truncated number or a partial parameter set."""
    async def scenario():
        client = HargassnerTelnetClient("test", firmware)
        message = temperature_message(client, "68.237")
        if split_at == "every_byte":
            chunks = [message[index:index + 1] for index in range(len(message))]
        else:
            split = {
                "prefix": 1,
                "number": message.index(b"68.237") + 3,
                "newline": len(message) - 1,
            }[split_at]
            chunks = [message[:split], message[split:]]
        updates = []
        client.register_callback(updates.append)
        await receive_chunks(client, chunks)
        assert len(updates) == 1
        assert updates[0]["TK"]["value"] == 68.237
        assert len(updates[0]) == len(client._parser.parameters)
        assert client.statistics["messages_parsed"] == 1
        assert client.statistics["last_message_length"] == client.expected_message_length

    asyncio.run(scenario())


def test_multiple_messages_and_partial_tail_keep_latest_values():
    """Coalesced reads retain every complete update and the unfinished tail."""
    async def scenario():
        client = HargassnerTelnetClient("test", "V14_1HAR_q1")
        first = temperature_message(client, 61)
        second = temperature_message(client, 62)
        third = temperature_message(client, "63.875")
        split = third.index(b"63.875") + 3
        updates = []
        client.register_callback(lambda data: updates.append(data["TK"]["value"]))
        await receive_chunks(client, [
            b"\r\nWelcome\r\n" + first + b" \n" + second + third[:split],
            third[split:],
        ])
        assert updates == [61, 62, 63.875]
        assert (await client.get_latest_data())["TK"]["value"] == 63.875
        assert client.statistics["messages_parsed"] == 3

    asyncio.run(scenario())


def test_read_timeout_preserves_unfinished_message():
    """A read timeout does not discard bytes from a still-open connection."""
    async def scenario():
        client = HargassnerTelnetClient("test", "V14_1HAR_q1")
        message = temperature_message(client, "68.237")
        split = message.index(b"68.237") + 3
        updates = []
        client.register_callback(lambda data: updates.append(data["TK"]["value"]))
        await receive_chunks(client, [message[:split], TimeoutError(), message[split:]])
        assert updates == [68.237]

    asyncio.run(scenario())


def test_disconnect_discards_partial_message_before_next_connection():
    """A new connection cannot finish or inherit the old connection's line."""
    async def scenario():
        client = HargassnerTelnetClient("test", "V14_1HAR_q1")
        message = temperature_message(client, "68.237")
        split = message.index(b"68.237") + 3
        updates = []
        client.register_callback(lambda data: updates.append(data["TK"]["value"]))
        await receive_chunks(client, [message[:split]])
        assert updates == []
        assert await client.get_latest_data() == {}
        assert client._buffer == b""
        await receive_chunks(client, [message[split:] + temperature_message(client, 72)])
        assert updates == [72]

    asyncio.run(scenario())
