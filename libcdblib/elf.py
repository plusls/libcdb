''' solve elf file'''
import mmap
import os

from elftools.elf.elffile import ELFFile
from elftools.elf.sections import SymbolTableSection

class ELF(ELFFile):
    '''Encapsulates information about an ELF file.'''
    def __init__(self, path):
        # elftools uses the backing file for all reads and writes
        # in order to permit writing without being able to write to disk,
        # mmap() the file.

        #: :class:`file`: Open handle to the ELF file on disk
        self.file = open(path,'rb')

        #: :class:`mmap.mmap`: Memory-mapped copy of the ELF file on disk
        self.mmap = mmap.mmap(self.file.fileno(), 0, access=mmap.ACCESS_COPY)

        super(ELF,self).__init__(self.mmap)

        #: :class:`str`: Path to the file
        self.path = os.path.abspath(path)

        #: :class:`dotdict` of ``name`` to ``address`` for all symbols in the ELF
        self.symbols = {}

        self.buildid = self._get_buildid()

        self._populate_symbols()

    @property
    def sections(self):
        """
        :class:`list`: A list of :class:`elftools.elf.sections.Section` objects
            for the segments in the ELF.
        """
        return list(self.iter_sections())

    def _get_buildid(self):
        """:class:`str`: GNU Build ID embedded into the binary"""
        section = self.get_section_by_name('.note.gnu.build-id')
        if section:
            raw_build_id = section.data()[16:]
            buildid = ''
            for ch in raw_build_id:
                buildid += '%02x' % ch
            return buildid
        return ''

    def _populate_symbols(self):
            """
            >>> bash = ELF(which('bash'))
            >>> bash.symbols['_start'] == bash.entry
            True
            """

            # Populate all of the "normal" symbols from the symbol tables
            for section in self.sections:
                if not isinstance(section, SymbolTableSection):
                    continue

                for symbol in section.iter_symbols():
                    value = symbol.entry.st_value
                    if not value or not symbol.name:
                        continue
                    self.symbols[symbol.name] = value
