import os
import json
import uuid

from datetime import datetime


class SessionManager:

    def __init__(self):

        self.chat_directory = "Chat_History"

        os.makedirs(
            self.chat_directory,
            exist_ok=True
        )

    # ---------------------------------------------------
    # Internal Helper
    # ---------------------------------------------------

    def _get_session_path(self, session_id):

        return os.path.join(
            self.chat_directory,
            f"{session_id}.json"
        )

    # ---------------------------------------------------
    # Create New Session
    # ---------------------------------------------------

    def create_session(
        self,
        documents,
        model,
        temperature,
        top_k
    ):

        session_id = str(uuid.uuid4())

        current_time = datetime.now().strftime(
            "%d-%m-%Y %H:%M:%S"
        )

        session_data = {

            "session_id": session_id,

            "title": "Chat",

            "created_at": current_time,

            "last_updated": current_time,

            "documents": documents,

            "config": {

                "model": model,

                "temperature": temperature,

                "top_k": top_k

            },

            "messages": []

        }

        self.save_session(
            session_id,
            session_data
        )

        return session_id

    # ---------------------------------------------------
    # Save Session
    # ---------------------------------------------------

    def save_session(
        self,
        session_id,
        session_data
    ):

        file_path = self._get_session_path(
            session_id
        )

        with open(
            file_path,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                session_data,
                file,
                indent=4,
                ensure_ascii=False
            )

    # ---------------------------------------------------
    # Load Session
    # ---------------------------------------------------

    def load_session(
        self,
        session_id
    ):

        file_path = self._get_session_path(
            session_id
        )

        if not os.path.exists(file_path):

            raise FileNotFoundError(
                f"Session '{session_id}' not found."
            )

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    # ---------------------------------------------------
    # Append Message
    # ---------------------------------------------------

    def append_message(
        self,
        session_id,
        role,
        content,
        sources=None
    ):

        session = self.load_session(
            session_id
        )

        message = {
            "role": role,
            "content": content
        }

        if role == "user":
            if session["title"] == "Chat":
                title = content.strip()

                if len(title) > 45:
                    title = title[:45] + "..."

                session["title"] = title

        if role == "assistant":

            message["sources"] = (
                sources if sources else []
            )

        session["messages"].append(
            message
        )

        session["last_updated"] = (
            datetime.now().strftime(
                "%d-%m-%Y %H:%M:%S"
            )
        )

        self.save_session(
            session_id,
            session
        )

    # ---------------------------------------------------
    # List All Sessions
    # ---------------------------------------------------

    def list_sessions(self):

        sessions = []

        for filename in os.listdir(
            self.chat_directory
        ):

            if not filename.endswith(".json"):
                continue

            filepath = os.path.join(
                self.chat_directory,
                filename
            )

            with open(
                filepath,
                "r",
                encoding="utf-8"
            ) as file:

                data = json.load(file)
            if not data.get("session_id"):
                continue

            sessions.append(
                {
                    "session_id":
                        data.get("session_id",""),

                    "title":
                        data.get("title", "New Chat"),

                    "documents":
                        data.get("documents", []),

                    "created_at":
                        data.get("created_at","01-07-2026 00:00:00"),

                    "last_updated":
                        data.get("last_updated","01-07-2026 00:00:00"),

                    "total_messages":
                        len(data.get("messages",[]))
                }
            )

        sessions.sort(
            key=lambda x:
                datetime.strptime(
                    x["last_updated"],
                    "%d-%m-%Y %H:%M:%S"
                ),
            reverse=True
        )

        return sessions

    # ---------------------------------------------------
    # Delete Session
    # ---------------------------------------------------

    def delete_session(
        self,
        session_id
    ):

        file_path = self._get_session_path(
            session_id
        )

        if not os.path.exists(file_path):
            raise FileNotFoundError(
                f"Session '{session_id}' not found."
            )
        os.remove(file_path)

    # ---------------------------------------------------
    # Rename Session
    # ---------------------------------------------------

    def rename_session(
        self,
        session_id,
        title
    ):

        session = self.load_session(
            session_id
        )

        session["title"] = title

        session["last_updated"] = (
            datetime.now().strftime(
                "%d-%m-%Y %H:%M:%S"
            )
        )

        self.save_session(
            session_id,
            session
        )