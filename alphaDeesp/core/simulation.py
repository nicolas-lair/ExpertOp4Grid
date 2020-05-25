from abc import ABC, abstractmethod
from math import fabs

import pandas as pd


class Simulation(ABC):
    """Abstract Class Simulation"""

    def __init__(self):
        super().__init__()

    @abstractmethod
    def build_powerflow_graph(self, raw_data):
        print("Abstract build_graph pre executed")
        """ returns a graph networkx """

    @abstractmethod
    def cut_lines_and_recomputes_flows(self, ids: list):
        """network is the grid in pypownet, XX in RTE etc..."""

    @abstractmethod
    def get_layout(self):
        """returns the layour of the graph in array of (x,y) form : [(x1,y1),(x2,y2)...]]"""

    @abstractmethod
    def get_substation_elements(self):
        """TODO"""

    @abstractmethod
    def get_substation_to_node_mapping(self):
        """TODO"""

    @abstractmethod
    def get_internal_to_external_mapping(self):
        """TODO"""

    @staticmethod
    def create_end_result_empty_dataframe():
        """This function creates initial structure for the dataframe"""

        end_result_dataframe_structure_initiation = {
            "overflow ID": ["XX"],
            "Flows before": ["XX"],
            "Flows after": [["X", "X", "X"]],
            "Delta flows": [["X", "X", "X"]],
            "Worsened line": [["X", "X", "X"]],
            "Prod redispatched": ["X"],
            "Load redispatched": ["X"],
            "Topology applied": ["X"],
            "Substation ID": ["X"],
            "Rank Substation ID": ["X"],
            "Topology score": ["X"],
            "Topology simulated score": ["X"],
            "Efficacity": ["X"],
        }
        end_result_data_frame = pd.DataFrame(end_result_dataframe_structure_initiation)

        return end_result_data_frame

    def create_df(self, d: dict, line_to_cut: list):
        """arg: d represents a topology"""
        # HERE WE CREATE DATAFRAME
        df = pd.DataFrame(d["edges"])
        pd.set_option("display.float_format", lambda x: "%.3f" % x)

        # takes a dataframe and swaps branches init_flows < 0
        self.branch_direction_swaps(df)

        new_flows = self.cut_lines_and_recomputes_flows(line_to_cut)
        # print("new simulated flows = ", new_flows)

        # here we multiply by (-1) new flows that are reversed
        n_flows = []
        for f, swapped in zip(new_flows, df["swapped"]):
            if swapped:
                n_flows.append(f * -1)
            else:
                n_flows.append(f)

        df["new_flows"] = n_flows

        # if new_flows < 0, and abs(new) > abs(init) then True (we invert edge direction) else False
        new_flows_swapped = []

        for i, row in df.iterrows():
            # if newf < 0. and fabs(new_flows) > fabs(initf):
            if row["new_flows"] < 0 and fabs(row["new_flows"]) > fabs(row["init_flows"]):
                new_flows_swapped.append(True)
            else:
                new_flows_swapped.append(False)

        df["new_flows_swapped"] = new_flows_swapped

        delta_flo = []

        # now we add delta flows
        # Si le flux a changé de direction, il y a 2 cas:
        # soit le nouveau flux est plus faible et dans ce cas, le report est négatif (on a déchargé la ligne) et le
        # report = abs(new_flows) - abs(init_flows)
        # sinon le report est positif et le report =
        # report = abs(new_flows) + abs(init_flows)
        for i, row in df.iterrows():
            if row["new_flows_swapped"]:
                delta_flo.append(fabs(row["new_flows"]) + fabs(row["init_flows"]))
                # here we swap origin and ext
                idx_or = row["idx_or"]
                df.at[i, "idx_or"] = row["idx_ex"]
                df.at[i, "idx_ex"] = idx_or
                df.at[i, "init_flows"] = fabs(row["init_flows"])
                # print(f"row #{i}, swapped idxor and idxer")
            else:
                delta_flo.append(fabs(row["new_flows"]) - fabs(row["init_flows"]))

        # delta_flows = self.df["new_flows"].abs() - self.df["init_flows"].abs()
        df["delta_flows"] = delta_flo

        # small modification test to have multiple components
        # self.df.set_value(0, "delta_flows", -32.)
        # self.df.set_value(4, "delta_flows", -42.)
        # self.df.set_value(5, "delta_flows", -22.)

        # DO NOT USE SET_VALUE ANYMORE, USE DF.AT INSTEAD
        # df.at[5, "delta_flows"] = -22.

        # now we identify gray edges
        gray_edges = []
        max_report = pd.DataFrame.max(df["delta_flows"].abs())
        # print("max = ", max_report)
        max_overload = max_report * float(self.param_options["ThresholdReportOfLine"])
        # print("max overload = ", max_overload)
        for edge_value in df["delta_flows"]:
            if fabs(edge_value) < max_overload:
                gray_edges.append(True)
            else:
                gray_edges.append(False)
        # print("gray edges = ", gray_edges)
        df["gray_edges"] = gray_edges

        # if self.debug:
        # print("==== After gray_edges added IN FUNCTION CREATE DF ====")
        print(df)

        return df

    @staticmethod
    def branch_direction_swaps(df):
        """we parse self.df and invert branches init_flows < 0"""
        swapped = []
        for i, row in df.iterrows():
            # print("i {} row {}".format(i, row))
            # a = row["delta_flows"]
            # b = row["final_delta_flows"]
            # if np.sign(a) != np.sign(b):

            a = row["init_flows"]
            if a < 0 and a != 0.:
                # here we swap origin and ext
                idx_or = row["idx_or"]
                df.at[i, "idx_or"] = row["idx_ex"]
                df.at[i, "idx_ex"] = idx_or
                df.at[i, "init_flows"] = fabs(row["init_flows"])
                # print(f"row #{i}, swapped idxor and idxer")
                swapped.append(True)
            else:
                swapped.append(False)

        df["swapped"] = swapped

    @staticmethod
    def invert_dict_keys_values(d):
        return dict([(v, k) for k, v in d.items()])
