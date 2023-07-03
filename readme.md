
# Chat cliente/servidor com Python


Este projeto foi criado para a disciplina de Sistemas Dsitribuídos e Sistemas Embarcados pela UFC, com foco em criar um chat entre 2 clientes usando um raspberry Pi como servidor em python.

![ufc](https://upload.wikimedia.org/wikipedia/commons/c/ce/Brasaoufc_horizontal.png)


# Passo a passo para executar
Primeiramente, saiba que este projeto pode ser replicado com qualquer computador e não apenas Raspberry, como foi o nosso caso.

1 - abra o terminal/cmd no diretório que o arquivo do servidor se encontra

execute o comando:

```python
python servidor.py
```



## cliente



2 - abra o terminal/cmd no diretório que o arquivo do cliente se encontra

executar o comando: 

```python
python cliente.py
```



3 - informe o nome de usuário e o ip do servidor e clique em entrar no chat

## Criando um programa executável
para criar um executável para o windows onde você não precisará executar o programa pelo terminal.

1 - primeiro precisa instalar o módulo pyinstaller  usando o seguinte comando:

```python
pip install pyinstaller
```



2 - verifique se tem o python instalado usando o comando:

```python
python --version
```

dessa forma ele vai mostrar qual a sua versão do python, assim confirmando que você tem ele instalado.



depois de confirmado que o python tá instalado e o pyinstaller foi instalado, você pode criar o executável

3 - verifique se está no mesmo diretório do cliente.py

4 - agora execute o comando a seguir:

```python
pyinstaller --onefile -w cliente.py
```



dessa forma você irá criar um executável a partir do seu cliente.py



o --onefile garante que o código vai encapsular todos os módulos necessários para a que o executável funcione de forma adequada.

AGORA BASTA VOCÊ USAR O SEU CHAT ;) 
    
## Acesse o site do projeto!
[acesse aqui](https://allmichel.github.io/Site_SE_SD/) nosso site, nele você vai encontrar nosso relatório, vídeos e muito mais!
## Links úteis

- Python. A referência da Linguagem Python. Disponível em: <https://docs.python.org/pt-br/3.11/reference/index.html#reference-index>. Acesso em: 20 jun. 2023

- Python. Socket - Low-Level networking interface. Disponível em: <https://docs.python.org/3.11/library/socket.html>. Acesso em: 20 jun. 2023


- Python. Threading - Thread-based parallelism. Disponível em: <https://docs.python.org/3.11/library/threading.html>. Acesso em: 20 jun. 2023


- Python. logging — Logging facility for Python. Disponível em: <https://docs.python.org/3/library/logging.html#module-logging>. Acesso em: 24 jun. 2023


- Python. Tkinter — Python interface to Tcl/Tk. Disponível em: <https://docs.python.org/3.11/library/tkinter.html#module-tkinter>. Acesso em: 25 jun. 2023

- Python. Select — Waiting for I/O completion. Disponível em: <https://docs.python.org/3.11/library/select.html#module-select>. Acesso em: 25 jun. 2023

## Autores
Este projeto foi feito por uma quipe de alunos da UFC - Universidade Federal do Ceará responsáveis por realizar o projeto final das Disciplinas de Sistemas Embarcados e Sistemas Distribídos. Ambas ministradas pelo [Prof. Juan Sebastian Toquica Arenas](https://www.linkedin.com/in/jstoquica/).

- [Allan Michel](https://www.linkedin.com/in/allmichel/)
- [Antonio Filipe](https://github.com/sousafilp)
- [Pedro Jonnathan](https://github.com/pjonnathan)

