#!/usr/bin/env python3

'''
systemandroid-decoder
Copyright (C) 2019-present  Kyle Alexander Buan

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
'''

# Show the title
print('SystemAndroid Video decoder')
print('Kyle Alexander Buan  2019/05/02\n')

# Get the input file path
infile = input('Drag&drop file to decode in this window then press ENTER.\n')

try:
    # Open the input file
    inf = open(infile, 'rb')

    print('Inspecting file...')

    # We check the first 4 bytes of the file
    inf.seek(4, 0)
    signature = inf.read(4)

    # If the first 4 bytes is NOT 'ftyp', then it's an not an MP4 container,
    # so we assume that it's either encrypted or not an MP4 video file.
    # If it is, then we can safely assume that it's an MP4 file,
    # but giving an MP4 file to this script is futile so why do that?
    if signature != b'ftyp':
        print('Okay, this looks password-protected (or is not a video file).')
    else:
        print('Wait, this is not password-protected. Why do that?')
        input()
        exit()

    print('Retrieving key...')

    # Now, we need to get the key used to encrypt the file.
    # Vault does exclusive or (XOR) for the first 128 bytes of the file to
    # "encrypt" the file. We need to know what value ("key")
    # was used to XOR those bytes.
    # However, since we know that the first byte of the original file is ASCII 'f'
    # (decimal 102) assuming it's an MP4 video file, then we can just XOR the first
    # "encrypted" byte of the file with decimal 102 to get the original value used to
    # XOR those bytes.
    key = signature[0] ^ ord('f')
    print('The key seems to be `' + str(key) + '`. Attempting to use that...')

    # Now that we have a guess at the key, let's try to XOR the first
    # four bytes of the encrypted file to see if we get back "ftyp" (which
    # means that we successfuly decoded an MP4 container)
    decoded_signature = bytes([signature[0] ^ key, signature[1] ^ key, signature[2] ^ key, signature[3] ^ key])
    if decoded_signature == b'ftyp':
        print('Yep, that looks like it! Trying to decode whole file...')
    else:
        print('Either the key retrieved is wrong, or you have given me a non-video file. Sorry, can\'t do.')
        input()
        exit()
    
    # Let's go back to the beginning of the encrypted file
    inf.seek(0, 0)

    # and prepare the output file (just append .mp4 to the original file name)
    outf = open(infile + '.mp4', 'wb')
    
    # then prepare the loop to decode the input
    currentbyte = inf.read(1)
    writtenbytes = 0

    while currentbyte:
        if writtenbytes < 0x80:
            # if we have read less than 128 bytes, then
            # XOR the input with the key before writing that byte
            # to the output
            resbyte = currentbyte[0] ^ key
        else:
            # else, we're already past 128 bytes, so
            # let's just output the byte as is
            resbyte = currentbyte[0]

        # write the decoded byte to the output
        outf.write(bytes([resbyte]))
        writtenbytes += 1

        # show some progress indicator in case the file is large
        # and takes time to process
        if writtenbytes % 1000000 == 0:
            print('Wrote ' + str(writtenbytes//1000000) + ' megabytes')

        # get the next byte and loop until the end of the file
        currentbyte = inf.read(1)

    # close the input and output files
    inf.close()
    outf.close()

    # and show a happy message.
    print('Operation done. Check the resulting file on the same folder as source.')
    input()
except IOError as error:
    # Oops, we got an error.
    print('Error:')
    print(str(error))
    print('Sorry.')
    input()