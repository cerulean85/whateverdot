import network as net
import config as cfg

if __name__ == '__main__':
    net.start_rpc_server(cfg.IP_DIRECTOR, cfg.PORT_DIRECTOR)


