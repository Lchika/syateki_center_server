import pings

# 死活監視のマシンのIPアドレス
# hosts = ["192.168.0.1", "192.168.0.2", "192.168.0.3"]


class Pings:
    __p = pings.Ping()

    def reached(self, hosts):
        results = []
        for h in hosts:
            res = self.__p.ping(h)
            if res.is_reached():
                results.append(True)
            else:
                results.append(False)
        return results
