import subprocess


class Pings:
    def is_connectable(self, host):
        ping = subprocess.Popen(["ping", "-w", "3", "-c", "1", host], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        ping.communicate()
        return ping.returncode == 0
    
    def scan(self, hosts):
        results = []
        for h in hosts:
            results.append(self.is_connectable(h))
        return results
