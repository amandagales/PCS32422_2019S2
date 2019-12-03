-- http://myfpgablog.blogspot.com/2011/12/memory-initialization-methods.html
library ieee;
--use ieee.std_logic_1164.ALL;
use ieee.numeric_bit.ALL;
--use std.textio.all;

entity fp_unity is 
    port (
    A,B : in bit_vector (63 downto 0); -- inputs
    op  : in bit_vector (10 downto 0); -- op for instr
    sh  : in bit_vector (5 downto 0);  -- shamt for instr
    O   : out bit_vector (63 downto 0);
    done : out bit                     -- can continue 
    );
end entity;


architecture structural of fp_unity is
begin
	done <= '0';
	O <= (others => '0');
end structural;