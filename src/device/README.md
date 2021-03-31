
# Device

Device modules are specific to laser cutting and the lower level interactions with laser cutter drivers. This includes the USB connections and connections to the CH341-chip through both the libUSB driver (`pyusb`) as well as any networked connections with laser-cutters.

This includes mock devices that are emulated for the purposes of compatibility or research.

# Lhystudios
These are the stock M2 Nano boards by Lhystudios and other closely related boards. This is the primary user of CH341 interfacing drivers. And the most complete driver availible. This includes parsing of Lhymicro-GL, production of Lhymicro-GL, channels of the data being sent over the USB. As well as emulation and parsing the commands.


# Moshi

Moshiboard classes are intended to deal with USB interactions to and from the CH341 chips on Moshiboards over USB. This is the result of `Project Moshi` (https://github.com/meerk40t/moshi) which seeks to reverse engineer the Moshiboard interactions. This provides functional Moshiboard drivers.
