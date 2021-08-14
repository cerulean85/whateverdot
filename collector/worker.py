from modules import network as net
import config as cfg

if __name__ == '__main__':
    net.start_rpc_server(cfg.IP_WORKER, cfg.PORT_WORKER)


