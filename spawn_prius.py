import subprocess
import os
import time
import signal


class Prius:
    def on_start(self):
        front_camera = self.get_port_info("front_camera/image_raw")["topic"]
        x = self.get_property("x")
        y = self.get_property("y")
        workspace_path = os.path.join(self.get_property("ws_path"), "")
        self.block_id = front_camera.split("/")[1]
        self.control_topic = self.get_port_info("prius")["topic"]
        if not os.path.isdir(workspace_path + "devel"):
            self.alert("Building ROS workspace", "INFO")
            subprocess.run(
                "cd {} && . /opt/ros/melodic/setup.sh && catkin_make".format(
                    workspace_path
                ),
                shell=True,
            )
        subprocess.Popen(
            "vglrun bash -c 'source {} && roslaunch car_demo spawn_prius.launch block_id:={} x:={} y:={} '".format(
                workspace_path + "devel/setup.bash", self.block_id, x, y
            ),
            shell=True,
        )
        time.sleep(15)
        print("run topic rely")
        self.relay_p = subprocess.Popen(
            "rosrun topic_tools relay {} {}".format(
                self.control_topic, "/" + self.block_id + "/prius"
            ),
            shell=True,
        )

