-- http://myfpgablog.blogspot.com/2011/12/memory-initialization-methods.html
library ieee;
--use ieee.std_logic_1164.ALL;
use ieee.numeric_bit.ALL;
--use std.textio.all;

entity rom is
  generic (
    addressSize : natural := 64;
    wordSize    : natural := 32;
    mifFileName : string  := "rom.dat"
  );
  port (
    addr : in  bit_vector(addressSize-1 downto 0);
    data : out bit_vector(wordSize-1 downto 0);
    hit  : out bit
  );
end rom;

architecture romhardcodded of rom is
type rom_data is array (0 to 49) of bit_vector ( wordSize - 1 downto 0 );
constant rom : rom_data := (
    x"91000C02", -- 0: addi x2, x0, #3
    x"00000000", -- 4: NOP
    x"00000000", -- 8: NOP
    x"00000000", -- C: NOP
    x"b4001042", --10: CBZ to #228 when x2 = 0
    x"D1000442", --14: sub x2, x2, #1
    x"00000000", --18: NOP
    x"00000000", --1C: NOP
    x"00000000", --20: NOP
    x"00000000", --24: NOP
    x"00000000", --28: NOP
    x"00000000", --2C: NOP
    x"00000000", --30: NOP
    x"17fffff5", --34: branch para a posi��o #18
    x"91000C01", --38: addi x1, x0, #3
    x"91000C01", --3C: addi x1, x0, #3
    x"91000C01", --40: addi x1, x0, #3
    x"91000C01", --40: addi x1, x0, #3
    x"00000000", --48: NOP
    x"00000000", --4C: NOP
    x"00000000", --50: NOP
    x"00000000", --54: NOP
    x"00000000", --58: NOP
    x"00000000", --5C: NOP
    x"00000000",  --NOP
    x"00000000",  --NOP
    x"00000000",  --NOP
    x"00000000",  --NOP
    x"00000000",  --NOP
    x"00000000",  --NOP
    x"00000000",  --NOP
    x"00000000",  --NOP
    x"00000000",  --NOP
    x"00000000",  --NOP
    x"00000000",  --NOP
    x"00000000",  --NOP
    x"00000000",  --NOP
    x"00000000",  --NOP
    x"00000000",  --NOP
    x"00000000",  --NOP
    x"00000000",  --NOP
    x"00000000",  --NOP
    x"00000000",  --NOP
    x"00000000",  --NOP
    x"00000000",  --NOP
    x"00000000",  --NOP
    x"00000000",  --NOP
    x"00000000",  --NOP
    x"00000000",  --NOP
    x"00000000"  --NOP
-- x"8B000020",  -- F add X0 = X1 + X0 00
-- x"00000000",
-- x"00000000",
-- x"00000000",
-- x"00000000",
-- x"b4000040", --CBZ to i+1           04
-- x"00000000",
-- x"00000000",
-- x"00000000",
-- x"00000000",
-- x"91000C00",  -- E addi x0 = x0 + 3
-- x"00000000",
-- x"00000000",
-- x"00000000",
-- x"00000000",
-- x"F9000FE0",  -- sw mem(sp +24 ) <= x0
-- x"00000000",
-- x"00000000",
-- x"00000000",
-- x"00000000",
-- x"00000000",
-- x"F94017E1", -- x1 <= mem(sp + 40) 
-- x"00000000",
-- x"00000000",
-- x"00000000",
-- x"00000000",
-- x"b5000040", --CBNZ to i+1 
-- x"8B000020",  -- F add X0 = X1 + X0 C
-- x"8B000020"  -- F add X0 = X1 + X0
-- --
-- --x"B1000C00",  -- D addis x0 = x0 + 3 set flags
-- --x"AB000020",  -- C add x0 = x1 + x0 set flags
-- --x"8A000020",  -- and
-- --x"B4000020", -- se x0 = 0 pula pra pc + 4
-- --
-- --
 --x"" x"8B000020",  -- F add X0 = X1 + X0
 --x"",
);
begin
    data <= rom(to_integer(unsigned(addr(31 downto 2))));
    hit <= '1'; --always hit
end architecture romhardcodded;
--architecture vendorfree of rom is
--  constant depth : natural := 2**10;
--  type mem_type is array (0 to depth-1) of bit_vector(wordSize-1 downto 0);

--  impure function init_mem(mif_file_name : in string) return mem_type is
--      file     mif_file : text open read_mode is mif_file_name;
--      variable mif_line : line;
--      variable temp_bv  : bit_vector(wordSize-1 downto 0);
--      variable temp_mem : mem_type;
--  begin
--      for i in mem_type'range loop
--          readline(mif_file, mif_line);
--   --report "mif_line = " & mif_line severity note; 
--          read(mif_line, temp_bv);
--   --report "The value of 'temp_bv' is" &integer'image(temp_bv); 
--          temp_mem(i) := temp_bv;
--      end loop;
--      return temp_mem;
--  end;
--  constant mem : mem_type := init_mem(mifFileName);
--begin
--  data <= mem(to_integer(unsigned(to_stdlogicvector(addr))));
--end vendorfree;
