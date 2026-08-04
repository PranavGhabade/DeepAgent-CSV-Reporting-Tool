"""
Shared Memory Store

Organized shared memory for all agents.
"""

from __future__ import annotations


class MemoryStore:

    def __init__(self):

        self.memory = {

            "dataset": {},

            "analysis": {},

            "reports": {},

            "metadata": {},

            # Conversation history
            "conversation": []
        }

    # ---------------- Dataset ----------------

    def store_dataset(self, key, value):
        self.memory["dataset"][key] = value

    def get_dataset(self, key):
        return self.memory["dataset"].get(key)

    # ---------------- Analysis ----------------

    def store_analysis(self, key, value):
        self.memory["analysis"][key] = value

    def get_analysis(self, key):
        return self.memory["analysis"].get(key)

    # ---------------- Reports ----------------

    def store_report(self, key, value):
        self.memory["reports"][key] = value

    def get_report(self, key):
        return self.memory["reports"].get(key)

    # ---------------- Metadata ----------------

    def store_metadata(self, key, value):
        self.memory["metadata"][key] = value

    def get_metadata(self, key):
        return self.memory["metadata"].get(key)

    # ---------------- Conversation ----------------

    def add_history(self, role: str, message: str):
        """
        Store one conversation turn.
        """

        self.memory["conversation"].append({
            "role": role,
            "message": message
        })

    def get_history(self):
        """
        Return the complete conversation history.
        """

        return self.memory["conversation"]

    def clear_history(self):
        """
        Remove all conversation history.
        """

        self.memory["conversation"] = []

    def latest_user_query(self):
        """
        Return the latest user message.
        """

        for message in reversed(self.memory["conversation"]):

            if message["role"] == "user":
                return message["message"]

        return ""

    def latest_assistant_response(self):
        """
        Return the latest assistant message.
        """

        for message in reversed(self.memory["conversation"]):

            if message["role"] == "assistant":
                return message["message"]

        return ""

    # ---------------- Utility ----------------

    def exists(self, key: str) -> bool:
        """
        Check whether an analysis result exists.
        """

        return self.get_analysis(key) is not None

    def available_analysis(self):
        """
        Return names of completed analyses.
        """

        return list(self.memory["analysis"].keys())

    # ---------------- Context Builders ----------------

    def planner_context(self):
        """
        Context required by the PlannerAgent.
        """

        return {
            "profile": self.get_analysis("profile"),
            "history": self.get_history(),
            "available_analysis": self.available_analysis(),
        }

    def statistics_context(self):
        """
        Context required by the StatisticsAgent.
        """

        return {
            "profile": self.get_analysis("profile"),
            "statistics": self.get_analysis("statistics"),
            "history": self.get_history(),
        }

    def visualization_context(self):
        """
        Returns the information required by the VisualizationAgent.
        """

        return {
            "profile": self.get_analysis("profile"),
            "statistics": self.get_analysis("statistics"),
            "visualizations": self.get_analysis("visualizations"),
            "history": self.get_history(),
        }

    def business_insight_context(self):
        """
        Returns the information required by the BusinessInsightAgent.
        """

        return {
            "profile": self.get_analysis("profile"),
            "statistics": self.get_analysis("statistics"),
            "visualizations": self.get_analysis("visualizations"),
            "history": self.get_history(),
        }
    

    def report_context(self):
        """
        Returns the information required by the ReportAgent.
        """

        return {
            "profile": self.get_analysis("profile"),
            "statistics": self.get_analysis("statistics"),
            "visualizations": self.get_analysis("visualizations"),
            "business_insights": self.get_analysis("business_insights"),
            "history": self.get_history(),
        }

    # ---------------- Generic ----------------

    def store(self, section, key, value):

        if section not in self.memory:
            self.memory[section] = {}

        self.memory[section][key] = value

    def retrieve(self, section, key):

        if section not in self.memory:
            return None

        return self.memory[section].get(key)

    # ---------------- Maintenance ----------------

    def clear(self):
        self.__init__()

    def keys(self):
        return self.memory.keys()

    def to_dict(self):
        return self.memory

    def __repr__(self):
        return f"MemoryStore(sections={list(self.memory.keys())})"