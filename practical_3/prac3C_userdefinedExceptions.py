class InvalidSPIError(Exception):
    pass


try:
    spi = float(input("Enter SPI: "))

    if spi < 0 or spi > 10:
        raise InvalidSPIError("SPI must be between 0 and 10.")

    print("Valid SPI:", spi)

except InvalidSPIError as e:
    print("User-defined exception:", e)