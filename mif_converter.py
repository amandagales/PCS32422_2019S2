from __future__ import print_function
from functools import reduce
import sys
import logging


# These dictionaries where based on this article:
# https://en.wikipedia.org/wiki/Executable_and_Linkable_Format

file_header_dict_32bits = {

    # This dictionary contains the File Header specifications for 32 bits configurations
    # Contents ordered in this fashion:
    #   addr: (size_in_bytes, [functions], (arguments)),
    # or
    #   addr: (size_in_bytes, function, (name, {dictionary})),

    # 0x7F followed by ELF(45 4c 46) in ASCII; these four bytes constitute the magic number.
    0x00: (4, ["equals", "and_func"], (0x7f, 0x45, 0x4c, 0x46)),

    # This byte is set to either 1 or 2 to signify 32- or 64-bit format, respectively.
    0x04: (1, "add_value_to_dict", ("EI_CLASS", {1: "32", 2: "64"})),

    # This byte is set to either 1 or 2 to signify little or big endianness, respectively.
    # This affects interpretation of multi-byte fields starting with offset 0x10.
    0x05: (1, "add_value_to_dict", ("EI_DATA", {1: "little", 2: "big"})),

    # Set to 1 for the original and current version of ELF.
    0x06: (1, "add_value_to_dict", ("EI_VERSION", {0: "", 1: "original"})),

    # Identifies the target operating system ABI.
    # It is often set to 0 regardless of the target platform.
    0x07: (1, "add_value_to_dict", ("EI_OSABI", {
        0x00: "System V",
        0x01: "HP-UX",
        0x02: "NetBSD",
        0x03: "Linux",
        0x04: "GNU Hurd",
        0x06: "Solaris",
        0x07: "AIX",
        0x08: "IRIX",
        0x09: "FreeBSD",
        0x0A: "Tru64",
        0x0B: "Novell Modesto",
        0x0C: "OpenBSD",
        0x0D: "OpenVMS",
        0x0E: "NonStop Kernel",
        0x0F: "AROS",
        0x10: "Fenix OS",
        0x11: "CloudABI",
    })),

    # Further specifies the ABI version. Its interpretation depends on the target ABI.
    0x08: (1, "add_key_to_dict", ("EI_ABIVERSION", {})),

    # Currently unused
    0x09: (7, "return_same_dict", ("EI_PAD", {})),

    # Identifies object file type.
    0x10: (2, "add_value_to_dict", ("e_type", {
        0x00: "ET_NONE",
        0x01: "ET_REL",
        0x02: "ET_EXEC",
        0x03: "ET_DYN",
        0x04: "ET_CORE",
        0xfe00: "ET_LOOS",
        0xfeff: "ET_HIOS",
        0xff00: "ET_LOPROC",
        0xffff: "ET_HIPROC",
    })),

    # Specifies target instruction set architecture.
    0x12: (2, "add_value_to_dict", ("e_machine", {
        0x00: "No specific instruction set",
        0x02: "SPARC",
        0x03: "x86",
        0x08: "MIPS",
        0x14: "PowerPC",
        0x16: "S390",
        0x28: "ARM",
        0x2A: "SuperH",
        0x32: "IA-64",
        0x3E: "x86-64",
        0xB7: "AArch64",
        0xF3: "RISC-V",
    })),

    # Set to 1 for the original version of ELF.
    0x14: (4, "add_value_to_dict", ("e_version", {0: "", 1: "original"})),

    # This is the memory address of the entry point from where the process starts executing.
    # This field is either 32 or 64 bits long depending on the format defined earlier.
    0x18: (4, "add_memory_value_to_dict", ("e_entry", {})),

    # Points to the start of the program header table. It usually follows the file header immediately,
    # making the offset 0x34 or 0x40 for 32- and 64-bit ELF executables, respectively.
    0x1c: (4, "add_memory_value_to_dict", ("e_phoff", {})),

    # Points to the start of the section header table.
    0x20: (4, "add_memory_value_to_dict", ("e_shoff", {})),

    # Interpretation of this field depends on the target architecture.
    0x24: (4, "add_memory_value_to_dict", ("e_flags", {})),

    # Contains the size of this header, normally 64 Bytes for 64-bit and 52 Bytes for 32-bit format.
    0x28: (2, "add_memory_value_to_dict", ("e_ehsize", {})),

    # Contains the size of a program header table entry.
    0x2a: (2, "add_memory_value_to_dict", ("e_phentsize", {})),

    # Contains the number of entries in the program header table.
    0x2c: (2, "add_memory_value_to_dict", ("e_phnum", {})),

    # Contains the size of a section header table entry.
    0x2e: (2, "add_memory_value_to_dict", ("e_shentsize", {})),

    # Contains the number of entries in the section header table.
    0x30: (2, "add_memory_value_to_dict", ("e_shnum", {})),

    # Contains index of the section header table entry that contains the section names.
    0x32: (2, "add_memory_value_to_dict", ("e_shstrndx", {})),

    # End of ELF Header (size) (EOF)
    0x34: (0, "nop", ("", {})),
}


file_header_dict_64bits = {

    # This dictionary contains the File Header specifications for 64 bits configurations
    # Contents ordered in this fashion:
    #   addr: (size_in_bytes, [functions], (arguments)),
    # or
    #   addr: (size_in_bytes, function, (name, {dictionary})),

    # 0x7F followed by ELF(45 4c 46) in ASCII; these four bytes constitute the magic number.
    0x00: (4, ["equals", "and_func"], (0x7f, 0x45, 0x4c, 0x46)),

    # This byte is set to either 1 or 2 to signify 32- or 64-bit format, respectively.
    0x04: (1, "add_value_to_dict", ("EI_CLASS", {1: "32", 2: "64"})),

    # This byte is set to either 1 or 2 to signify little or big endianness, respectively.
    # This affects interpretation of multi-byte fields starting with offset 0x10.
    0x05: (1, "add_value_to_dict", ("EI_DATA", {1: "little", 2: "big"})),

    # Set to 1 for the original and current version of ELF.
    0x06: (1, "add_value_to_dict", ("EI_VERSION", {0: "", 1: "original"})),

    # Identifies the target operating system ABI.
    # It is often set to 0 regardless of the target platform.
    0x07: (1, "add_value_to_dict", ("EI_OSABI", {
        0x00: "System V",
        0x01: "HP-UX",
        0x02: "NetBSD",
        0x03: "Linux",
        0x04: "GNU Hurd",
        0x06: "Solaris",
        0x07: "AIX",
        0x08: "IRIX",
        0x09: "FreeBSD",
        0x0A: "Tru64",
        0x0B: "Novell Modesto",
        0x0C: "OpenBSD",
        0x0D: "OpenVMS",
        0x0E: "NonStop Kernel",
        0x0F: "AROS",
        0x10: "Fenix OS",
        0x11: "CloudABI",
    })),

    # Further specifies the ABI version. Its interpretation depends on the target ABI.
    0x08: (1, "add_key_to_dict", ("EI_ABIVERSION", {})),

    # Currently unused
    0x09: (7, "return_same_dict", ("EI_PAD", {})),

    # Identifies object file type.
    0x10: (2, "add_value_to_dict", ("e_type", {
        0x00: "ET_NONE",
        0x01: "ET_REL",
        0x02: "ET_EXEC",
        0x03: "ET_DYN",
        0x04: "ET_CORE",
        0xfe00: "ET_LOOS",
        0xfeff: "ET_HIOS",
        0xff00: "ET_LOPROC",
        0xffff: "ET_HIPROC",
    })),

    # Specifies target instruction set architecture.
    0x12: (2, "add_value_to_dict", ("e_machine", {
        0x00: "No specific instruction set",
        0x02: "SPARC",
        0x03: "x86",
        0x08: "MIPS",
        0x14: "PowerPC",
        0x16: "S390",
        0x28: "ARM",
        0x2A: "SuperH",
        0x32: "IA-64",
        0x3E: "x86-64",
        0xB7: "AArch64",
        0xF3: "RISC-V",
    })),

    # Set to 1 for the original version of ELF.
    0x14: (4, "add_value_to_dict", ("e_version", {0: "", 1: "original"})),

    # This is the memory address of the entry point from where the process starts executing.
    # This field is either 32 or 64 bits long depending on the format defined earlier.
    0x18: (8, "add_memory_value_to_dict", ("e_entry", {})),

    # Points to the start of the program header table. It usually follows the file header immediately,
    # making the offset 0x34 or 0x40 for 32- and 64-bit ELF executables, respectively.
    0x20: (8, "add_memory_value_to_dict", ("e_phoff", {})),

    # Points to the start of the section header table.
    0x28: (8, "add_memory_value_to_dict", ("e_shoff", {})),

    # Interpretation of this field depends on the target architecture.
    0x30: (4, "add_memory_value_to_dict", ("e_flags", {})),

    # Contains the size of this header, normally 64 Bytes for 64-bit and 52 Bytes for 32-bit format.
    0x34: (2, "add_memory_value_to_dict", ("e_ehsize", {})),

    # Contains the size of a program header table entry.
    0x36: (2, "add_memory_value_to_dict", ("e_phentsize", {})),

    # Contains the number of entries in the program header table.
    0x38: (2, "add_memory_value_to_dict", ("e_phnum", {})),

    # Contains the size of a section header table entry.
    0x3a: (2, "add_memory_value_to_dict", ("e_shentsize", {})),

    # Contains the number of entries in the section header table.
    0x3c: (2, "add_memory_value_to_dict", ("e_shnum", {})),

    # Contains index of the section header table entry that contains the section names.
    0x3e: (2, "add_memory_value_to_dict", ("e_shstrndx", {})),

    # End of ELF Header (size) (EOF)
    0x40: (0, "nop", ("", {})),
}


program_header_dict_32bits = {

    # This dictionary contains the Program Header specifications for 32 bits configurations
    # Contents ordered in this fashion:
    #   addr: (size_in_bytes, [functions], (arguments)),
    # or
    #   addr: (size_in_bytes, function, (name, {dictionary})),

    # Identifies the type of the segment.
    0x00: (4, "add_value_to_dict", ("p_type", {
        0x00000000: "PT_NULL",
        0x00000001: "PT_LOAD",
        0x00000002: "PT_DYNAMIC",
        0x00000003: "PT_INTERP",
        0x00000004: "PT_NOTE",
        0x00000005: "PT_SHLIB",
        0x00000006: "PT_PHDR",
        0x60000000: "PT_LOOS",
        0x6FFFFFFF: "PT_HIOS",
        0x70000000: "PT_LOPROC",
        0x7FFFFFFF: "PT_HIPROC",
    })),

    # Offset of the segment in the file image.
    0x04: (4, "add_memory_value_to_dict", ("p_offset", {})),

    # Virtual address of the segment in memory.
    0x08: (4, "add_memory_value_to_dict", ("p_vaddr", {})),

    # On systems where physical address is relevant, reserved for segment's physical address.
    0x0c: (4, "add_memory_value_to_dict", ("p_paddr", {})),

    # Size in bytes of the segment in the file image. May be 0.
    0x10: (4, "add_memory_value_to_dict", ("p_filesz", {})),

    # Size in bytes of the segment in memory. May be 0.
    0x14: (4, "add_memory_value_to_dict", ("p_memsz", {})),

    # Segment-dependent flags (position for 32-bit structure).
    0x18: (4, "add_memory_value_to_dict", ("p_flags", {})),

    # 0 and 1 specify no alignment. Otherwise should be a positive,
    # integral power of 2, with p_vaddr equating p_offset modulus p_align.
    0x1c: (4, "add_memory_value_to_dict", ("p_align", {})),

    # End of Program Header (size) (EOF)
    0x20: (0, "nop", ("", {})),
}


program_header_dict_64bits = {

    # This dictionary contains the Program Header specifications for 64 bits configurations
    # Contents ordered in this fashion:
    #   addr: (size_in_bytes, [functions], (arguments)),
    # or
    #   addr: (size_in_bytes, function, (name, {dictionary})),

    # Identifies the type of the segment.
    0x00: (4, "add_value_to_dict", ("p_type", {
        0x00000000: "PT_NULL",
        0x00000001: "PT_LOAD",
        0x00000002: "PT_DYNAMIC",
        0x00000003: "PT_INTERP",
        0x00000004: "PT_NOTE",
        0x00000005: "PT_SHLIB",
        0x00000006: "PT_PHDR",
        0x60000000: "PT_LOOS",
        0x6FFFFFFF: "PT_HIOS",
        0x70000000: "PT_LOPROC",
        0x7FFFFFFF: "PT_HIPROC",
    })),

    # Segment-dependent flags (position for 64-bit structure).
    0x04: (4, "add_memory_value_to_dict", ("p_flags", {})),

    # Offset of the segment in the file image.
    0x08: (8, "add_memory_value_to_dict", ("p_offset", {})),

    # Virtual address of the segment in memory.
    0x10: (8, "add_memory_value_to_dict", ("p_vaddr", {})),

    # On systems where physical address is relevant, reserved for segment's physical address.
    0x18: (8, "add_memory_value_to_dict", ("p_paddr", {})),

    # Size in bytes of the segment in the file image. May be 0.
    0x20: (8, "add_memory_value_to_dict", ("p_filesz", {})),

    # Size in bytes of the segment in memory. May be 0.
    0x28: (8, "add_memory_value_to_dict", ("p_memsz", {})),

    # 0 and 1 specify no alignment. Otherwise should be a positive,
    # integral power of 2, with p_vaddr equating p_offset modulus p_align.
    0x30: (8, "add_memory_value_to_dict", ("p_align", {})),

    # End of Program Header (size) (EOF)
    0x38: (0, "nop", ("", {})),
}


section_header_dict_32bits = {

    # This dictionary contains the Section Header specifications for 32 bits configurations
    # Contents ordered in this fashion:
    #   addr: (size_in_bytes, [functions], (arguments)),
    # or
    #   addr: (size_in_bytes, function, (name, {dictionary})),

    # An offset to a string in the .shstrtab section that represents the name of this section.
    0x00: (4, "add_memory_value_to_dict", ("sh_name", {})),

    # Identifies the type of this header.
    0x04: (4, "add_value_to_dict", ("sh_type", {
        0x0: "SHT_NULL",
        0x1: "SHT_PROGBITS",
        0x2: "SHT_SYMTAB",
        0x3: "SHT_STRTAB",
        0x4: "SHT_RELA",
        0x5: "SHT_HASH",
        0x6: "SHT_DYNAMIC",
        0x7: "SHT_NOTE",
        0x8: "SHT_NOBITS",
        0x9: "SHT_REL",
        0x0A: "SHT_SHLIB",
        0x0B: "SHT_DYNSYM",
        0x0E: "SHT_INIT_ARRAY",
        0x0F: "SHT_FINI_ARRAY",
        0x10: "SHT_PREINIT_ARRAY",
        0x11: "SHT_GROUP",
        0x12: "SHT_SYMTAB_SHNDX",
        0x13: "SHT_NUM",
        0x60000000: "SHT_LOOS",
    })),

    # Identifies the attributes of the section.
    0x08: (4, "add_value_to_dict", ("sh_flags", {
        0x1: "SHF_WRITE",
        0x2: "SHF_ALLOC",
        0x4: "SHF_EXECINSTR",
        0x10: "SHF_MERGE",
        0x20: "SHF_STRINGS",
        0x40: "SHF_INFO_LINK",
        0x80: "SHF_LINK_ORDER",
        0x100: "SHF_OS_NONCONFORMING",
        0x200: "SHF_GROUP",
        0x400: "SHF_TLS",
        0x0ff00000: "SHF_MASKOS",
        0xf0000000: "SHF_MASKPROC",
        0x4000000: "SHF_ORDERED",
        0x8000000: "SHF_EXCLUDE",
    })),

    # Virtual address of the section in memory, for sections that are loaded.
    0x0c: (4, "add_memory_value_to_dict", ("sh_addr", {})),

    # Offset of the section in the file image.
    0x10: (4, "add_memory_value_to_dict", ("sh_offset", {})),

    # Size in bytes of the section in the file image. May be 0.
    0x14: (4, "add_memory_value_to_dict", ("sh_size", {})),

    # Contains the section index of an associated section.
    # This field is used for several purposes, depending on the type of section.
    0x18: (4, "add_memory_value_to_dict", ("sh_link", {})),

    # Contains extra information about the section.
    # This field is used for several purposes, depending on the type of section.
    0x1c: (4, "add_memory_value_to_dict", ("sh_info", {})),

    # Contains the required alignment of the section. This field must be a power of two.
    0x20: (4, "add_memory_value_to_dict", ("sh_addralign", {})),

    # Contains the size, in bytes, of each entry, for sections that contain fixed-size entries.
    # Otherwise, this field contains zero.
    0x24: (4, "add_memory_value_to_dict", ("sh_entsize", {})),

    # End of Section Header (size) (EOF)
    0x28: (0, "nop", ("", {})),
}


section_header_dict_64bits = {

    # This dictionary contains the Section Header specifications for 64 bits configurations
    # Contents ordered in this fashion:
    #   addr: (size_in_bytes, [functions], (arguments)),
    # or
    #   addr: (size_in_bytes, function, (name, {dictionary})),

    # An offset to a string in the .shstrtab section that represents the name of this section.
    0x00: (4, "add_memory_value_to_dict", ("sh_name", {})),

    # Identifies the type of this header.
    0x04: (4, "add_value_to_dict", ("sh_type", {
        0x0: "SHT_NULL",
        0x1: "SHT_PROGBITS",
        0x2: "SHT_SYMTAB",
        0x3: "SHT_STRTAB",
        0x4: "SHT_RELA",
        0x5: "SHT_HASH",
        0x6: "SHT_DYNAMIC",
        0x7: "SHT_NOTE",
        0x8: "SHT_NOBITS",
        0x9: "SHT_REL",
        0x0A: "SHT_SHLIB",
        0x0B: "SHT_DYNSYM",
        0x0E: "SHT_INIT_ARRAY",
        0x0F: "SHT_FINI_ARRAY",
        0x10: "SHT_PREINIT_ARRAY",
        0x11: "SHT_GROUP",
        0x12: "SHT_SYMTAB_SHNDX",
        0x13: "SHT_NUM",
        0x60000000: "SHT_LOOS",
    })),

    # Identifies the attributes of the section.
    0x08: (8, "add_value_to_dict", ("sh_flags", {
        0x1: "SHF_WRITE",
        0x2: "SHF_ALLOC",
        0x4: "SHF_EXECINSTR",
        0x10: "SHF_MERGE",
        0x20: "SHF_STRINGS",
        0x40: "SHF_INFO_LINK",
        0x80: "SHF_LINK_ORDER",
        0x100: "SHF_OS_NONCONFORMING",
        0x200: "SHF_GROUP",
        0x400: "SHF_TLS",
        0x0ff00000: "SHF_MASKOS",
        0xf0000000: "SHF_MASKPROC",
        0x4000000: "SHF_ORDERED",
        0x8000000: "SHF_EXCLUDE",
    })),

    # Virtual address of the section in memory, for sections that are loaded.
    0x10: (8, "add_memory_value_to_dict", ("sh_addr", {})),

    # Offset of the section in the file image.
    0x18: (8, "add_memory_value_to_dict", ("sh_offset", {})),

    # Size in bytes of the section in the file image. May be 0.
    0x20: (8, "add_memory_value_to_dict", ("sh_size", {})),

    # Contains the section index of an associated section.
    # This field is used for several purposes, depending on the type of section.
    0x28: (4, "add_memory_value_to_dict", ("sh_link", {})),

    # Contains extra information about the section.
    # This field is used for several purposes, depending on the type of section.
    0x2c: (4, "add_memory_value_to_dict", ("sh_info", {})),

    # Contains the required alignment of the section. This field must be a power of two.
    0x30: (8, "add_memory_value_to_dict", ("sh_addralign", {})),

    # Contains the size, in bytes, of each entry, for sections that contain fixed-size entries.
    # Otherwise, this field contains zero.
    0x38: (8, "add_memory_value_to_dict", ("sh_entsize", {})),

    # End of Section Header (size) (EOF)
    0x40: (0, "nop", ("", {})),
}


log_format = "%(asctime)s - %(levelname)s: %(message)s"
logging.basicConfig(filename='mif_converter.log', filemode='w', level=logging.DEBUG, format=log_format)


class AssertingTools:
    @staticmethod
    def equals(x, y):
        return x == y

    @staticmethod
    def and_func(x, y):
        return x and y

    @staticmethod
    def nop(*args, **kwargs):
        pass

    @staticmethod
    def return_same_dict(config_dictionary, *args, **kwargs):
        return config_dictionary

    @staticmethod
    def add_value_to_dict(config_dictionary, key, value, *args, **kwargs):
        config_dictionary[key] = value
        return config_dictionary

    @staticmethod
    def add_key_to_dict(config_dictionary, key, memory_value, *args, **kwargs):
        config_dictionary[key] = hex(int(memory_value, 16))
        return config_dictionary

    @staticmethod
    def add_memory_value_to_dict(config_dictionary, key, value, memory_value, *args, **kwargs):
        config_dictionary[key] = memory_value
        return config_dictionary


def multi_byte_concat(config_dictionary, focused_bytes):
    if config_dictionary["EI_DATA"] == 'big':
        return str(reduce(lambda first_val, sec_val: first_val + sec_val, focused_bytes))
    else:
        return str(reduce(lambda first_val, sec_val: sec_val + first_val, focused_bytes))


def get_file_name():
    try:
        file_name = sys.argv[1]
    except IndexError as e:
        print("\nError: pass a file name as an argument to this program!\n")
        print("Try something like: python " + sys.argv[0] + " program.o\n")
        logging.exception("Error: pass a file name as an argument to this program!")
        raise e
    else:
        elf_extensions = ["o", "axf", "bin", "elf", "prx", "puff", "ko", "mod", "so"]
        if len(file_name.split(".")) == 1 or file_name.split(".")[-1].lower() not in elf_extensions:
            print("\nWarning: file given may not be an Executable and Linkable Format (ELF)!\n")
            logging.warning("file given may not be an Executable and Linkable Format (ELF)!")

    return file_name


def open_file(file_name):

    # Leitura do arquivo em Python 2
    if sys.version_info[0] < 3:
        with open(file_name, 'r') as f:
            hex_str_list = ["{:02x}".format(ord(c)) for c in f.read()]

    # Leitura do arquivo em Python 3
    else:
        with open(file_name, 'rb') as f:
            hex_str_list = ["{:02x}".format(c) for c in f.read()]

    hex_list = [hex(int(x, 16)) for x in hex_str_list]
    # logging.debug("hex_list = " + str(hex_list))

    return hex_str_list, hex_list


def parse_dict(hex_str_list, hex_list, CONFIGURATION_DICT, file_dict_32bits, file_dict_64bits, offset=0):
    PC = 0x00
    eof = False
    while not eof:
        if CONFIGURATION_DICT["EI_CLASS"] == '32':
            size, functions, values_tuple = file_dict_32bits[PC]
        else:
            size, functions, values_tuple = file_dict_64bits[PC]

        focused_bytes = hex_str_list[PC + offset:PC + offset + size]
        int_focused_bytes = [int(x, 16) for x in hex_list[PC + offset:PC + offset + size]]

        # EOF
        if size == 0:
            logging.info("Reached EOF.")
            break

        logging.info("PC = " + str(hex(PC)))
        logging.info("PC + offset = " + str(hex(PC + offset)))
        logging.info("focused_bytes = " + str(focused_bytes))
        logging.info("int_focused_bytes = " + str(int_focused_bytes))

        if type(functions) == list:
            map_function, reduce_function = functions

            logging.info("values_tuple = " + str(values_tuple))
            logging.debug("map_list = " + str(list(map(getattr(AssertingTools, map_function), int_focused_bytes, values_tuple))))

            result = reduce(getattr(AssertingTools, reduce_function), map(getattr(AssertingTools, map_function), int_focused_bytes, values_tuple))
            logging.info("result = " + str(result))

        else:
            logging.info("values_tuple = " + str(values_tuple))

            key, dictionary = values_tuple
            function = getattr(AssertingTools, functions)
            logging.info("key = " + str(key))
            logging.info("function: " + functions)

            multi_bytes = multi_byte_concat(CONFIGURATION_DICT, focused_bytes)
            logging.info("multi_bytes = " + str(multi_bytes))

            value = dictionary.get(int(multi_bytes, 16))
            logging.info("value = " + str(value))

            CONFIGURATION_DICT = function(config_dictionary=CONFIGURATION_DICT, key=key, value=value, instruction_dictionary=dictionary, memory_value=multi_bytes)
            logging.debug("CONFIGURATION_DICT = " + str(CONFIGURATION_DICT))

            # print(CONFIGURATION_DICT)

        PC += size

        print("PC = " + str(PC) + " (" + str(hex(PC)) + "); with offset: " + str(PC + offset) + " (" + str(hex(PC + offset)) + ")")

    return CONFIGURATION_DICT


def write_mif_file(config_dictionary, file_name, parsed_instructions):
    DEPTH = int(config_dictionary['EI_CLASS'])  # The size of data in bits
    WIDTH = int(DEPTH / 8)  # The size of memory in words
    initial_address = int(config_dictionary['e_entry'], 16)  # Where the program starts to be written in memory

    file_name = file_name.split(".")[0] + ".mif"

    with open(file_name, 'w') as f:
        f.write("DEPTH = %d;\n" % (DEPTH))
        f.write("WIDTH = %d;\n" % (WIDTH))
        f.write("ADDRESS_RADIX = HEX;\n")
        f.write("DATA_RADIX = HEX;\n")
        f.write("CONTENT\n")
        f.write("BEGIN\n")
        for index, value in enumerate(parsed_instructions):
            f.write(str(hex(initial_address + index))[2:] + "\t:\t" + value + ";\n")
        f.write("END;\n")


def main():
    file_name = get_file_name()
    hex_str_list, hex_list = open_file(file_name)

    # Inicialization with default values
    CONFIGURATION_DICT = {
        "EI_CLASS": "64",
        "EI_DATA": "big",
        "EI_VERSION": "original",
        "EI_OSABI": "",
    }

    # File Header
    CONFIGURATION_DICT = parse_dict(hex_str_list, hex_list, CONFIGURATION_DICT, file_header_dict_32bits, file_header_dict_64bits)

    # Program Header
    program_header_offset = int(CONFIGURATION_DICT["e_ehsize"], 16)
    program_header_size = int(CONFIGURATION_DICT["e_phentsize"], 16)

    if program_header_size > 0:
        CONFIGURATION_DICT = parse_dict(hex_str_list, hex_list, CONFIGURATION_DICT, program_header_dict_32bits, program_header_dict_64bits, offset=program_header_offset)
    # /Program Header

    # Section Header
    section_header_offset = program_header_offset + program_header_size
    section_header_size = int(CONFIGURATION_DICT["e_shentsize"], 16)

    if section_header_size > 0:
        CONFIGURATION_DICT = parse_dict(hex_str_list, hex_list, CONFIGURATION_DICT, section_header_dict_32bits, section_header_dict_64bits, offset=section_header_offset)
    # /Section Header

    # Reading Data
    data_offset = section_header_offset + section_header_size
    data_hex = hex_str_list[data_offset:]

    word_size = int(int(CONFIGURATION_DICT['EI_CLASS']) / 8)

    eof = False
    parsed_instructions = []
    while not eof:
        if data_offset + word_size < len(data_hex):
            multi_byte = multi_byte_concat(CONFIGURATION_DICT, data_hex[data_offset:data_offset + word_size])
        else:
            multi_byte = multi_byte_concat(CONFIGURATION_DICT, data_hex[data_offset:])
            eof = True

        parsed_instructions.append(multi_byte)
        data_offset += word_size
    # /Reading Data

    # MIF Convertion
    write_mif_file(CONFIGURATION_DICT, file_name, parsed_instructions)


if __name__ == "__main__":
    main()
