from app import app
from omegaconf import OmegaConf

if __name__ == '__main__':
    cfg = OmegaConf.load('config/config.yml')
    app.run(
        debug=cfg.debug,
        host=cfg.services.host,
        port=cfg.services.port
    )
