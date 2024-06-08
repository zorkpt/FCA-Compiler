import os
import subprocess

# dir onde estão os arquivos .fca
input_dir = './exemplos'
output_dir = './outputs'

# Cria o diretório de saída se não existir
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Encontra todos os arquivos .fca no diretório especificado
input_files = [f for f in os.listdir(input_dir) if f.endswith('.fca')]

main_script = 'main.py'


# Função para correr um teste
def run_test(input_file):
    input_path = os.path.join(input_dir, input_file)
    output_file = input_file.replace('.fca', '.txt')
    output_path = os.path.join(output_dir, output_file)

    # Executa o script Python principal com o arquivo de entrada e redireciona a saída para o arquivo de saída
    with open(output_path, 'w') as outfile:
        subprocess.run(['python3', main_script, input_path], stdout=outfile)


# corre os testes para todos os files .fca
for input_file in input_files:
    run_test(input_file)
    print(f'Teste executado para {input_file}, ver o resultado em {output_dir}/{input_file.replace(".fca", ".txt")}')

print('Todos os testes foram executados.')
