import asyncio
import datetime
import json
from prompt_toolkit import HTML
 
from .. import config
from ..decorators import handler_class, handler
from .. import utils
from . import basic_spectral_sequence
from ..channel import Channel

@handler_class 
class SpectralSequenceChart(Channel):
    def __init__(self, name, sseq=None):
        super().__init__(name) 
        self.name = name
        if sseq:
            self.sseq = sseq
        else:
            self.sseq = basic_spectral_sequence.BasicSpectralSequenceChart(name)
        # self.handshakes = set()

    @handler
    async def handle_new_user(self, data, text):
        await self.send_to_user(data["user_id"], utils.json_stringify({
            "cmd" : "accept_user",
            "state" : self.sseq
        }))

    @handler
    async def handle_client_error(self, data, text):
        utils.print_error("Client sent an error: " + data["error"])


    def print_started_msg(self):
        colored_url = f"<blue>http://localhost:{config.PORT}/sseq/{self.name}</blue>"
        utils.format_and_print_text(
                f"""<green>Started spectral sequence "{self.name}".\n""" +\
                f"""Visit "{colored_url}" to view.</green>"""
        )

    async def add_class(self, x : int, y : int, **kwargs):
        kwargs.update({"x" : x, "y" : y, "node_list" : [0]})
        c = self.sseq.add_class(**kwargs)
        kwargs.update({"id" : c.id})
        handshake = await self.broadcast("add_class", kwargs)#, True)
        # await handshake
        return c  

    async def add_edge(self, edge_type, source, target, **kwargs):
        kwargs.update({"type" : edge_type, "source" : source, "target" : target})
        e = self.sseq.add_edge(edge_type, **kwargs)
        kwargs.update({"id" : e.id, "source" : source.id, "target" : target.id})
        await self.broadcast("add_edge", kwargs)
        return e

    async def add_structline(self, source, target, **kwargs):
        await self.add_edge("structline",source, target, **kwargs)

    def get_class_by_idx(self, x, y, idx):
        return self.sseq._classes_by_bidegree.get((x,y), [])[idx]

    def get_classes_in_bidegree(self, x, y):
        return self.sseq._classes_by_bidegree.get((x,y), [])

    def set_x_range(self, x_min, x_max):
        self.sseq.xRange = [x_min, x_max]

    def set_y_range(self, y_min, y_max):
        self.sseq.yRange = [y_min, y_max]

    def set_initial_x_range(self, x_min, x_max):
        self.sseq.initialxRange = [x_min, x_max]        

    def set_initial_y_range(self, y_min, y_max):
        self.sseq.initialyRange = [y_min, y_max]


        