#include <stdio.h>
#include <stdlib.h>
#include "projet.h" 

/* ⚠️ Il y a des free en plus ce qui pose une erreur a la fin. Tout ca c'est a cause des allocations dynamiques 
    qu'on free qui nous suit des lee debut*/
int main()
{
    const char *filename = "program.txt";

    // 1. On cree un programme assembleur
    FILE *fp = fopen(filename, "w");
    if (!fp)
    {
        perror("Erreur lors de la création du fichier");
        return 1;
    }

    // 2. On ecrit .DATA and .CODE
    fprintf(fp,
            ".DATA\n"
            "a DW 5\n"
            "b DB 10, 20\n"
            ".CODE\n"
            "MOV AX, a\n"
            "ADD AX, b\n"
            "CMP AX, 15\n"
            "JZ ok\n"
            "MOV BX, 0\n"
            "JMP end\n"
            "ok: MOV BX, 99\n"
            "end: HALT\n");
    fclose(fp);

    // 3. on parse le fichier
    ParserResult *res = parse(filename);
    if (!res)
    {
        fprintf(stderr, "Erreur de parsing\n");
        return 1;
    }
    printf("res->code_count = %d\n", res->code_count);


    // 4. On remplace les lebaels et les variables par leurs emplacements memoire
    int replaced = resolve_constants(res);
    printf("Remplacements effectués : %d\n", replaced);

    // 5. Init CPU
    CPU *cpu = cpu_init(64);
    if (!cpu)
    {
        fprintf(stderr, "Erreur d'initialisation du CPU\n");
        free_parser_result(res);
        return 1;
    }

    // 6. On charge la mémoire et les instructions
    allocate_variables(cpu, res->data_instructions, res->data_count);
    allocate_code_segment(cpu, res->code_instructions, res->code_count);
    printf("=== Instructions in CS ===\n");

    Segment *cs = hashmap_get(cpu->memory_handler->allocated, "CS");

    if (!cs)
    {
        printf("Erreur: segment CS introuvable\n");
        return 1; 
    }

    printf("=== Instructions in CS ===\n");
    for (int i = 0; i < cs->size; i++)
    {
        Instruction *instr = (Instruction *)load(cpu->memory_handler, "CS", i);
        if (instr)
        {
            printf("[%d] %s %s %s\n", i,
                   instr->mnemonic ? instr->mnemonic : "(null)",
                   instr->operand1 ? instr->operand1 : "(null)",
                   instr->operand2 ? instr->operand2 : "(null)");
        }
        else
        {
            printf("[%d] NULL instruction\n", i);
        }
    }

    // 7. Run the program
    run_program(cpu);

    // 8. clean
    cpu_destroy(cpu);
    free_parser_result(res);
    return 0;
}
