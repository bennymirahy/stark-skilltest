import os
import starkbank

project = starkbank.Project(
    environment="sandbox",
    id="6264161537359872",
    private_key=os.getenv("PRIVATE_KEY")
)
