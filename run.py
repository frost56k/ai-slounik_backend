# -*- coding: utf-8 -*-
#!/usr/bin/env python3
import logging
from app import create_app

app = create_app()

if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    logging.info("Start server on 5000...")
    app.run(port=5000, debug=True)
