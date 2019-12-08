	.arch armv8-a
	.file	"ff.c"
	.text
	.align	2
	.global	factorial
	.type	factorial, %function
factorial:
	stp x29, x30, [sp, -32]! 
        add x29, sp, 0 
        ldur w0, [x29, 28] 
        bne .L2 
        mov w0, 1 
        b .L3 
.L2: 
        ldur w0, [x29, 28] 
        sub w0, w0, #1 
        bl factorial 
        mov w1, w0 
        ldur w0, [x29, 28] 
        mul w0, w1, w0 
.L3: 
        ldur x29, [sp,#0] 
        ldur x30, [sp,#8] 
        br x30 
	.size	factorial, .-factorial
	.align	2
	.global	main
	.type	main, %function

main:
		stp 	x29, x30, [sp, -32]! 
        add 	x29, sp, 0 
        mov 	w0, 4 
        ldur 	w0, [x29, 24] 
        bl 	factorial 
        mov 	w0, 0 
        ldur 	x29, [sp,#0] 
        ldur 	x30, [sp,#8] 
        br 	x30 

	.size	main, .-main
	.ident	"GCC: (Ubuntu/Linaro 7.4.0-1ubuntu1~18.04.1) 7.4.0"
	.section	.note.GNU-stack,"",@progbits
