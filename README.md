# Jusbrasil Crawler Challenge

> Resolução
> do [Desafio Software Engineer Intern](https://gist.github.com/diegoramosdev/4d6946efe20441d142e37f7510cbb3db)
---

## 💻 Instalando dependências do projeto

A aplicação foi desenvolvida em Python 3, utilizando a
biblioteca [BeautifulSoup4](https://beautiful-soup-4.readthedocs.io/en/latest/).

As dependências do projeto estão listadas no arquivo `requirements.txt`. Para instalá-las utilizando o `pip`, basta
executar o comando a
seguir:

````commandline
pip install -r requirements.txt
````

---

## 🚀 Executando projeto localmente

> Por favor, nos informe quais são as instruções necessárias para rodar sua solução.

Para usar <nome_do_projeto>, siga estas etapas:

```
<exemplo_de_uso>
```

Adicione comandos de execução e exemplos que você acha que os usuários acharão úteis. Fornece uma referência de opções
para pontos de bônus!

---

## ❗ Informações complementares

> Nesta seção estão respondidas demais informações solicitadas junto com a resolução do desafio.

### 📆 Prazos:

- **Data de início:** ``22/06/2023``
- **Data de conclusão:** ``26/06/2023``
- **Data de submissão:** ``DD/06/2023``

### ⏰ Tempo investido:

- **Desenvolver os requisitos mínimos da aplicação:** ``7 horas e 20 min``

<img src="assets/forest.png " alt="Descrição da imagem" width="350" height="350">

- **Documentação, refinamentos e melhorias:** ``X horas e Y min``

### 🔨 Ajustes e melhorias

> O que você não incluiu em sua solução que gostaria que soubéssemos: Você estava com pouco tempo e não conseguiu
> incluir algo?
> Outras informações sobre sua solução que você acha que seria importante sabermos (se aplicável).

O projeto ainda está em desenvolvimento e as próximas atualizações serão voltadas nas seguintes tarefas:

- [x] Extrair dados
- [x] Salvar dados extraídos num único arquivo JSON
    - [ ] Inserir caminho onde deve ser salvos os dados pelo terminal
- [x] Melhorar tratamento dos dados
- [ ] Enriquecer dados
    - [x] Validação do formato de datas
- [ ] Escrever documentação
    - [ ] README.md
    - [ ] Doc strings em funções
- [ ] Tratamento de exceções
    - [ ] O que fazer se houver erro ao tentar escrever no arquivo JSON?
- [ ] Testes unitários
- [ ] Aplicação em paradgima POO

### 🕵️‍♂️ Suposições assumidas:

> Use essa seção para nos contar sobre qualquer suposição que tenha assumido ao criar sua solução.

Antes de construir o crawler, precisei pensar em estratégias que poderia utilizar para extrair os dados solicitados da
página fornecida. Para isso, no primeiro momento, utilizei algum tempo para inspecionar a estrutura do HTML da página
com o intuito de perceber alguns padrões ou quais eram os níveis de profundidade onde estavam essas informações.

Nesse processo, notei duas coisas me ajudaram a traçar uma estratégia:

1. As informações desejadas estavam dentro de tags `table` e estas, por sua vez, estavam agrupadas em uma `div`
   identificada por um ``id``. Assim, consegui mapear uma estrutura na qual poderia reduzir meu problema. De modo
   simplificado, segue a estrutura mapeada:

````html

<div id="divDadosResultado-A">
    <table>
        <tr>
            <td></td> <!-- Index da tabela que continha as informações = Informação irrelevante para o caso -->
            <td>
                <span></span>
                <table> <!-- Tabela com as informações de jurisprudência -->
                    <tr>
                        <td>
                            <!-- Outras tags -->
                        </td>
                    </tr>
                    <tr>
                        <td></td>
                    </tr>
                    <!-- Outras tags tr -->
                </table>
            </td>
        </tr>
    </table>
</div>
````

2. Analisando a primeira tag ``<table>`` desta ``div``, é possível perceber que suas linhas são compostas de número que
   representa o índice, e de outras tabelas, onde estão localizadas as informações das jurisprudências. Nessas
   tags `table`, pude notar que todas as informações que precisaria extrarir estavam dentro de uma "etiquetas"
   (**Ementa:**, **Classe / Assunto:**, etc.). Logo, poderia utilizar esse padrão para extrair a informação. Nesse ponto
   havia outros dois possíveis caminhos:
    1. Navegar pelo HTML até o nível da ``<div id="divDadosResultado-A">`` e, então, utilizar Expressões Regulares a fim
       de identificar o padrão dessas etiquetas ou
    2.

Se não fossem essas "etiquetas", seria necessário identificar algum outro padrão a nível de tag para que, usando o
BeautilfulSoup, pudesse atingir as informações.

No arquivo JSON, cada objeto que representa um jurisprudência possui os atributos ``dataPublicacao``
e ``dataJulgamento``. Como essas informações são obtidas como strings durante a extração, julguei interessante criar uma
função responsável por verificá-las a fim de saber se tratam de datas válidas ou não, armazenando esta
informação em atributos extras, nomeados de ``_dataPublicacaoValida`` e ``_dataJulgamentoValida``, respectivamente.

### 🔀 Atalhos realizados:

> Se aplicável, você fez algo que sentiu que poderia ter feito melhor em uma aplicação do "mundo real"?

Como neste cenário existia esse padrão das "etiquetas", preferi adotar essa estratégia. Porém, algumas vezes me
questionei se num cenário do "mundo real" o ideal seria não depender desses padrões textuais e fosse preferível fazer um
crawler que navegasse a nível de estrutura de página.

### 💬 Feedbacks:

> Você tem algum feedback para tornarmos esse desafio melhor? Por favor, nos conte. :)

Até que me diverti fazendo o desafio. Achei tanto o objetivos quanto as orientações bem claras. Então, semana de
mesmo estando em semana de avaliações na faculdade (final de semestre) isso me ajudou aentender o que deveria ser feito.

Além disso, aproveitei a oportunidade para iniciar a leitura do
livro [Web Scraping com Python](https://www.amazon.com.br/Web-Scraping-Com-Python-Coletando/dp/8575227300/ref=sr_1_8?__mk_pt_BR=%C3%85M%C3%85%C5%BD%C3%95%C3%91&crid=3LL9RB4MO701K&keywords=python&qid=1687927515&sprefix=pytho%2Caps%2C232&sr=8-8),
que havia comprado há um tempinho atrás. Então, fui aprendendo algumas coisas no caminho (Primeira vez que apliquei
regex) e foi interessante ver que consegui pôr ... num desafio prático.

[⬆ Voltar ao topo](#jusbrasil-crawler-challenge)<br>

