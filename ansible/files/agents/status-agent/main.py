
import sh
from action.comm import global_comm
from action.knowledge_base import local_neo4j
import time

if __name__ == "__main__":
    with global_comm() as lcomm:
        while True:
            lcomm.publish("status", {
                "agent":"sphere-host",
                "status":"running",
            })
            print("[debug] [life cycle] restarting loop")
            time.sleep(5)
            