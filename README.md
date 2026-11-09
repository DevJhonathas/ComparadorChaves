# Manual do Usuário — Comparador de Chaves

Este manual explica como baixar, abrir e utilizar o **Comparador de Chaves**, aplicativo desktop desenvolvido em Python para comparar chaves de acesso de NF-e armazenadas em um banco de dados com as chaves encontradas em arquivos XML.

> **Importante:** o programa compara somente as chaves de acesso. Ele não compara o conteúdo integral das notas fiscais e não altera, insere ou exclui registros do banco de dados.

## 1. O que o aplicativo faz

O Comparador de Chaves:

1. Conecta ao banco de dados informado pelo usuário.
2. Consulta a coluna escolhida, na tabela configurada, para obter as chaves de acesso.
3. Percorre os arquivos `.xml` da pasta selecionada.
4. Em cada NF-e compatível, procura o elemento `infNFe` e lê seu atributo `Id`.
5. Remove o prefixo `NFe` do atributo `Id` e valida a chave extraída.
6. Compara as chaves encontradas nos XMLs com as chaves obtidas do banco.
7. Apresenta os resultados e permite exportá-los.

### Como a chave é extraída

O XML de uma NF-e contém um elemento semelhante a este:

```xml
<infNFe Id="NFe[44 dígitos da chave de acesso]">
```

O aplicativo lê o atributo `Id`, remove o prefixo `NFe` e utiliza o restante como chave de acesso. Para NF-e, o valor esperado possui **exatamente 44 dígitos**.

No banco de dados, a coluna deve conter somente os 44 dígitos, sem o prefixo `NFe`. Recomenda-se que essa coluna seja de tipo textual (`VARCHAR`, `CHAR` ou equivalente), para preservar eventuais zeros à esquerda.

O aplicativo não deve completar, truncar ou aproximar chaves inválidas. Um valor com quantidade de dígitos diferente do esperado deve ser tratado como inválido.

## 2. Baixar o aplicativo pelo GitHub Releases

As versões executáveis do Comparador de Chaves serão publicadas na seção **Releases** do repositório dedicado à distribuição do programa no GitHub.

1. Acesse o repositório oficial de distribuição do Comparador de Chaves.
2. Abra a seção **Releases**.
3. Entre na versão mais recente, identificada como *Latest* quando essa indicação estiver disponível.
4. Na seção **Assets**, localize o arquivo executável do Comparador de Chaves, com extensão `.exe`.
5. Clique no arquivo `.exe` para baixá-lo.

**Atenção:** baixe o executável publicado em **Assets** da versão. Não selecione os arquivos automáticos `Source code (zip)` ou `Source code (tar.gz)`: eles contêm o código-fonte do repositório, não são o aplicativo pronto para uso.

Antes de executar, confira se está baixando o arquivo da página oficial de Releases do projeto e se a versão corresponde à publicação desejada.

## 3. Preparar e abrir o executável

### 3.1. Salvar o arquivo

1. Após o download, localize o arquivo `.exe`, normalmente na pasta **Downloads**.
2. Crie uma pasta para guardar o aplicativo, se desejar, por exemplo:

```text
C:\Users\SeuUsuario\Aplicativos\ComparadorDeNotas
```

3. Mova o executável baixado para essa pasta.

Como a distribuição é feita no modo **onefile**, o aplicativo é fornecido em um único executável. Não é necessário extrair uma pasta `.dist`, copiar bibliotecas ao lado do programa ou manter uma pasta de dependências distribuída separadamente.

### 3.2. Executar

1. Dê dois cliques no arquivo `.exe` baixado.
2. Aguarde a inicialização do aplicativo. Na primeira abertura, o programa pode demorar um pouco mais porque o empacotador prepara temporariamente os componentes internos necessários à execução.
3. Quando a janela do Comparador de Chaves aparecer, o aplicativo estará pronto para ser utilizado.

O modo `onefile` extrai automaticamente os componentes internos para uma área temporária do Windows durante a execução. Essa operação é feita pelo próprio programa; o usuário não precisa localizar, abrir ou copiar esses arquivos temporários.

**Não exclua arquivos temporários enquanto o aplicativo estiver aberto.** Feche o programa normalmente antes de realizar qualquer limpeza de arquivos temporários do Windows.

### 3.3. O computador precisa ter Python?

Não. O executável `onefile` reúne o aplicativo, o interpretador Python e as dependências incluídas durante a compilação. Portanto, não é necessário instalar Python para utilizar uma distribuição completa e corretamente compilada.

Entretanto, alguns bancos dependem de componentes externos do Windows, como drivers ODBC ou bibliotecas de cliente. Esses componentes não são necessariamente incorporados ao executável e podem precisar ser instalados separadamente. Consulte a seção [4. Bancos de dados e dependências](#4-bancos-de-dados-e-dependências).

### 3.4. Avisos do Windows

O Windows pode exibir o Microsoft Defender SmartScreen ou outro aviso ao executar um programa baixado da internet, especialmente quando o executável não possui assinatura digital reconhecida.

Antes de prosseguir, confira se o arquivo foi baixado da página oficial de Releases do projeto e se corresponde à versão publicada. Não execute arquivos cuja origem não seja confiável. Se houver dúvida sobre a autenticidade do arquivo, interrompa a execução e solicite confirmação ao responsável pelo projeto.

Não é necessário executar o aplicativo como administrador para o uso normal, a menos que o administrador do ambiente determine o contrário.

## 4. Bancos de dados e dependências

O projeto utiliza SQLAlchemy para organizar a comunicação com diferentes bancos. A disponibilidade de cada SGBD depende de o driver correspondente ter sido incluído na versão executável e, em alguns cenários, de componentes adicionais instalados no Windows.

| Banco | Informações e dependências |
|---|---|
| SQLite | Informe o caminho do arquivo `.db` ou `.sqlite`. Não exige servidor. O suporte utiliza o módulo SQLite do Python. |
| PostgreSQL | Informe host, porta, banco, usuário e senha. O driver `psycopg` precisa estar incluído na versão distribuída. |
| MySQL | Informe host, porta, banco, usuário e senha. O driver `PyMySQL` precisa estar incluído na versão distribuída. |
| SQL Server (MSSQL) | Pode exigir o `pyodbc` incluído na distribuição e um driver ODBC do SQL Server instalado no Windows. Informe o driver correto quando o formulário oferecer esse campo. |
| Oracle | O driver `oracledb` precisa estar incluído. Dependendo do modo de conexão e da configuração do ambiente, pode ser necessário instalar/configurar o Oracle Instant Client. |

**Atenção:** a arquitetura do aplicativo permite integrar esses bancos, mas isso não significa que todos estejam automaticamente disponíveis ou tenham sido validados no ambiente da sua empresa. Consulte as notas da versão (*Release notes*) para saber quais drivers foram incluídos e quais requisitos externos são necessários. Teste a conexão com o SGBD que será utilizado antes de executar uma comparação.

### 4.1. SQLite

Para SQLite:

- **Tipo/Driver:** SQLite.
- **Arquivo do banco:** caminho completo do arquivo `.db` ou `.sqlite`.
- **Host, porta, usuário e senha:** normalmente não são necessários.

Exemplo de caminho:

```text
C:\Dados\notas.db
```

### 4.2. Bancos com servidor

Para PostgreSQL, MySQL, SQL Server ou Oracle, normalmente serão solicitados:

| Campo | O que informar |
|---|---|
| Tipo de banco/driver | O SGBD utilizado. |
| Host/Servidor | Nome DNS ou endereço do servidor. |
| Porta | Porta de conexão configurada no servidor. |
| Banco/Service name | Nome do banco, serviço ou identificador solicitado pelo driver. |
| Usuário | Usuário autorizado a consultar os dados. |
| Senha | Senha desse usuário. |
| Driver ODBC | Quando aplicável, nome do driver ODBC instalado no Windows. |

Use os dados fornecidos pelo administrador do banco. Não tente adivinhar porta, nome do serviço ou driver.

## 5. Configurar o banco de dados

Na tela de configurações, selecione o tipo de banco correspondente ao ambiente que será consultado. Os campos exibidos podem variar conforme o banco selecionado. Preencha somente os campos aplicáveis.

1. Selecione o SGBD.
2. Informe o caminho do arquivo, no caso de SQLite, ou os dados do servidor, nos demais casos.
3. Informe usuário, senha e demais parâmetros solicitados.
4. Informe a tabela que contém as notas ou chaves.
5. Informe a coluna que armazena a chave de acesso.
6. Utilize a opção **Salvar configurações**, caso esteja disponível na tela.
7. Se o aplicativo perguntar se deseja salvar a senha, confirme somente se estiver em um computador confiável e autorizado.

As configurações comuns podem ser persistidas para uso posterior. A senha deve ser armazenada pelo mecanismo seguro de credenciais do sistema, e não em texto puro em um arquivo compartilhado.

> As configurações e credenciais são armazenadas no perfil do usuário do Windows. Ao utilizar outra conta do Windows ou outro computador, talvez seja necessário configurar novamente a conexão e informar a senha.

## 6. Informar a tabela e a coluna de chaves

A tabela e a coluna precisam corresponder exatamente à estrutura do banco.

Exemplo ilustrativo:

| Configuração | Exemplo |
|---|---|
| Tabela | `documentos` |
| Coluna | `chave_acesso` |

Os nomes acima são exemplos. Utilize os nomes reais do seu banco de dados.

A coluna deve armazenar a chave como texto, preferencialmente com 44 caracteres. Evite tipos numéricos, pois uma chave de acesso é um identificador, não um valor para cálculos; a conversão numérica pode remover zeros à esquerda ou causar perda de precisão.

**Permissões recomendadas:** utilize um usuário de banco com permissão somente de leitura (`SELECT`) sobre a tabela/coluna necessária. O comparador não precisa de permissão para inserir, alterar ou excluir registros.

## 7. Selecionar a pasta dos arquivos XML

1. Localize a seção de arquivos XML na tela de configurações.
2. Clique no botão para selecionar pasta, normalmente identificado por um ícone de pasta ou pela opção **Procurar**.
3. Escolha a pasta onde estão armazenados os XMLs.
4. Confirme a seleção.
5. Se houver a opção **Incluir subpastas**, habilite-a quando os XMLs também estiverem em diretórios internos.

Exemplo:

```text
D:\Fiscal\XML\2026
```

O aplicativo precisa ter permissão de leitura na pasta e nos arquivos. Arquivos em unidades de rede dependem de a unidade estar acessível para o usuário do Windows que abriu o programa.

## 8. Testar a conexão

Antes de iniciar uma comparação:

1. Confira o tipo de banco selecionado.
2. Revise host, porta, banco, usuário, senha e driver, quando aplicáveis.
3. Confira o nome da tabela e da coluna.
4. Clique em **Testar conexão**.
5. Aguarde a mensagem de sucesso ou de erro.

Se o teste falhar:

- Confirme se o servidor está ligado e acessível.
- Confira host e porta.
- Verifique usuário, senha e permissões.
- Confirme se o nome do banco/serviço está correto.
- No SQL Server, confira se o driver ODBC indicado está instalado.
- No Oracle, confira os requisitos do driver e a configuração de conexão.
- Confirme se o computador possui acesso à rede ou VPN necessária.

O teste de conexão não substitui a validação da consulta à tabela e à coluna. Caso a conexão funcione, mas a comparação apresente erro, confira os nomes dos objetos e as permissões de leitura.

## 9. Executar a comparação

Depois de configurar o banco e a pasta de XMLs:

1. Salve as configurações, se aplicável.
2. Confirme que o teste de conexão foi concluído com sucesso.
3. Confirme que a pasta selecionada contém os XMLs desejados.
4. Clique em **Iniciar comparação**.
5. Aguarde o processamento. A interface deve apresentar o andamento, quando essa informação estiver disponível.
6. Não feche o aplicativo enquanto a operação estiver em andamento.

Durante a operação, o programa consulta as chaves do banco, percorre os XMLs, extrai as chaves válidas e executa a comparação. O processamento ocorre em segundo plano para evitar, em condições normais, que a janela fique bloqueada.

## 10. Entender a extração da chave no XML

Para NF-e, o extrator procura o elemento `infNFe` e lê o atributo `Id`.

Exemplo ilustrativo:

```xml
<infNFe Id="NFe[44 dígitos da chave de acesso]">
```

Etapas realizadas:

1. Ler o atributo `Id`.
2. Verificar o prefixo `NFe`.
3. Remover somente esse prefixo.
4. Validar se o valor restante contém exatamente 44 dígitos.
5. Usar a chave resultante na comparação.

O programa não deve completar, truncar ou aproximar chaves inválidas. Uma chave com quantidade de dígitos diferente do esperado deve ser tratada como inválida, em vez de ser modificada automaticamente.

## 11. Entender os resultados

A comparação pode apresentar as seguintes situações:

| Situação | Significado |
|---|---|
| **Encontrada** | A chave está presente no banco e em pelo menos um XML válido. |
| **Somente no banco** | A chave está no banco, mas não foi encontrada nos XMLs lidos. |
| **Somente nos XMLs** | A chave foi encontrada em um XML, mas não consta no conjunto consultado no banco. |
| **XML inválido/erro de leitura** | O arquivo não pôde ser interpretado ou não forneceu uma chave válida. |
| **Duplicidade** | A mesma chave aparece mais de uma vez em uma das origens, conforme a contagem apresentada pelo aplicativo. |

### Exemplo

Considere estas chaves fictícias:

**Banco:**

```text
CHAVE_A
CHAVE_B
CHAVE_C
```

**XMLs:**

```text
nota_01.xml -> CHAVE_A
nota_02.xml -> CHAVE_C
nota_03.xml -> CHAVE_D
```

Resultado esperado:

| Chave | Resultado |
|---|---|
| CHAVE_A | Encontrada |
| CHAVE_B | Somente no banco |
| CHAVE_C | Encontrada |
| CHAVE_D | Somente nos XMLs |

Os valores acima são ilustrativos; as chaves reais de NF-e devem obedecer ao formato de 44 dígitos.

### Atenção ao interpretar “Somente no banco”

Esse status significa que a chave não foi localizada entre os XMLs que o aplicativo conseguiu processar na pasta selecionada. Antes de concluir que o documento não existe, confira se:

- A pasta escolhida é a correta.
- Os XMLs estão acessíveis.
- A opção de incluir subpastas foi utilizada quando necessária.
- Os arquivos correspondem ao mesmo período e universo de dados consultado no banco.
- Não houve erros de leitura ou arquivos ignorados.

## 12. Exportar os resultados

Se a versão instalada apresentar a opção **Exportar CSV**:

1. Aguarde a comparação terminar.
2. Clique em **Exportar CSV**.
3. Escolha a pasta e o nome do arquivo.
4. Confirme o salvamento.
5. Abra o CSV em um editor de planilhas ou de texto para analisar os resultados.

O CSV pode ser utilizado para filtrar, ordenar e compartilhar o resultado da conferência. Antes de compartilhar, verifique se o arquivo contém dados fiscais ou informações que devam permanecer restritas.

## 13. Atualizar o aplicativo

As novas versões serão publicadas na seção **Releases** do repositório oficial no GitHub.

1. Feche o Comparador de Chaves, caso esteja aberto.
2. Acesse a seção **Releases** do repositório.
3. Abra a versão mais recente.
4. Na seção **Assets**, baixe o novo arquivo `.exe`.
5. Salve o executável atualizado na pasta em que deseja manter o aplicativo.
6. Execute o novo arquivo.

Como a aplicação é distribuída em um único executável, não é necessário substituir uma pasta `.dist` nem copiar bibliotecas. Você pode manter a versão anterior até confirmar que a nova versão está funcionando; depois, pode removê-la.

As configurações e credenciais salvas no perfil do Windows normalmente permanecem disponíveis entre atualizações, desde que a nova versão mantenha os mesmos identificadores de organização e aplicação. Por segurança, mantenha uma cópia das configurações necessárias e esteja preparado para informar novamente a senha se o Windows ou o aplicativo solicitar.

Consulte o `CHANGELOG` ou as notas da Release para conhecer alterações, correções, requisitos e possíveis mudanças de compatibilidade.

## 14. Encerrar o aplicativo

1. Aguarde qualquer comparação em andamento terminar ou utilize a opção própria de cancelamento, se disponível.
2. Feche a janela pelo botão **X**.
3. Aguarde o encerramento do programa.

Não é necessário encerrar o processo pelo Gerenciador de Tarefas em uma utilização normal.

## 15. Solução de problemas

| Problema | O que verificar |
|---|---|
| O executável não abre | Confirme se o download terminou corretamente. Baixe novamente o arquivo `.exe` da Release oficial. Verifique se o antivírus colocou o arquivo em quarentena. |
| O Windows exibe um aviso de segurança | Confirme a origem do download e a versão publicada. Não execute o arquivo se não conseguir verificar sua procedência. |
| A primeira inicialização demora | No modo `onefile`, os componentes internos são preparados em uma área temporária. Aguarde e verifique se o antivírus não está examinando ou bloqueando o executável. |
| Mensagem de DLL ou biblioteca ausente | A versão pode não conter uma dependência necessária ou o ambiente pode exigir um componente externo. Consulte as notas da Release e solicite suporte. |
| Janela do CMD aparece | A versão pode ter sido compilada com console habilitado. Informe o responsável pela distribuição para verificar a opção Nuitka `--windows-console-mode=disable`. |
| Falha ao conectar ao banco | Confira servidor, porta, credenciais, rede, driver e permissões. |
| Tabela ou coluna não encontrada | Confira os nomes exatos no banco e se o usuário possui permissão de leitura. |
| Nenhuma chave encontrada nos XMLs | Confira se os arquivos são NF-e compatíveis com o extrator e se possuem `infNFe@Id` no formato esperado. |
| XML inválido | Verifique se o arquivo está íntegro, completo e codificado corretamente. Consulte a lista de erros, se disponível. |
| Chave aparece como não encontrada | Confirme a pasta, o período, a tabela, a coluna e se a chave está armazenada com 44 dígitos, sem o prefixo `NFe`. |
| Aplicativo fecha durante o processamento | Consulte os logs, se habilitados, e tente reproduzir com uma pasta menor para isolar o problema. |

## 16. Boas práticas e segurança

- Baixe o executável somente da seção **Releases** do repositório oficial.
- Utilize uma conta de banco com permissão somente de leitura.
- Não compartilhe senhas em capturas de tela, mensagens ou arquivos de configuração.
- Não publique XMLs reais ou CSVs com dados fiscais em repositórios públicos.
- Faça testes iniciais com cópias de arquivos e um banco de homologação, quando possível.
- Mantenha o executável em uma pasta local com permissões adequadas.
- Faça backup dos arquivos importantes antes de executar procedimentos de manutenção.
- Confira erros de leitura antes de interpretar os resultados como uma ausência definitiva.
- Preserve as chaves como texto para evitar perda de zeros à esquerda.
- Não interrompa a execução apagando manualmente a pasta temporária utilizada pelo programa.

## 17. Diagnóstico e suporte

Ao solicitar suporte, informe:

1. Versão do aplicativo, conforme indicada na Release baixada.
2. Versão do Windows.
3. SGBD utilizado e sua versão, se conhecida.
4. Etapa em que ocorreu o problema.
5. Mensagem de erro completa.
6. Quantidade aproximada de registros no banco e arquivos XML processados.

Não envie senhas, dados de acesso, XMLs reais ou informações fiscais sensíveis. Quando for necessário compartilhar um XML para diagnóstico, utilize um exemplo fictício ou mascare os dados mantendo a estrutura do documento.

---

**Comparador de Chaves — Manual do Usuário**  
Aplicativo desktop distribuído em um único executável para Windows (*onefile*).  
As versões oficiais são disponibilizadas na seção **Releases** do repositório do projeto no GitHub.
