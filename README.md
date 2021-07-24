# systemandroid-decoder

This script tries to read a `.bin` file created by the Android
application "Vault" and tries to extract a video from it.

## How does it work?

Vault, while looking like a secure data storage application,
is totally not secure at all. It does not encrypt files in the
traditional sense, but just runs the file's first 128 bytes
into an exclusive OR with a specific byte value used as key.

We cannot be sure what that byte value key is, but if we were to
assume that the `.bin` file contains a video, and assuming
that video is in an MP4 container, then the first 4 bytes of the file
should be `ftyp`. We can determine the byte value used as key
by finding out what value can be XOR-ed with `ftyp` to get the
value stored in the input file.

Fortunately, XOR is a reversible operation, meaning,

```
A XOR B is equal to C;
and
C XOR B is equal to A;
```

So we just do

```
(first byte of the file) XOR (the ASCII value of 'f') = the key
```

Now that we have a clue at the possible key, we can just try XOR-ing
the first 128 bytes of the file before copying
to the output and then for the remaining bytes of the
input file, just copy them as is to the output.

## How do I use this?

Just run the script through Python3 and it should give you instructions.

| Operating System | Running instructions |
| --- | --- |
| Windows | Install Python3 then double click the `.py` file. Then, type the path to the input file (relative or absolute) or drag-and-drop the input file to the terminal window then press `ENTER`. |
| Linux | Install Python3 (for example, `pacman -S python`) and then run the script (for example, `chmod +x sadecode.py && ./sadecode.py`). Type the path to the input file (relative or absolute) or drag-and-drop the input file to the terminal window then press `ENTER`. |
| macOS | Install Python3 (for example, via Brew) and then run the script (for example, `python3 sadecode.py`). Type the path to the input file (relative or absolute) or drag-and-drop the input file to the terminal window then press `ENTER`. |

## License

This is licensed with GPL-3. Please check the `LICENSE` file for more details.

Copyright (c) 2019-present  Kyle Alexander Buan