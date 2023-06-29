# Jusbrasil Crawler Challenge

> Resolução
> do [Desafio Software Engineer Intern](https://gist.github.com/diegoramosdev/4d6946efe20441d142e37f7510cbb3db)
---

## 🚀 Executando o projeto localmente

> Por favor, nos informe quais são as instruções necessárias para rodar sua solução.

### 💻 Instalando dependências do projeto

A aplicação foi desenvolvida em **Python 3**, utilizando a versão ``3.13.3`` da linguagem. A biblioteca
[**BeautifulSoup4**](https://beautiful-soup-4.readthedocs.io/en/latest/), na versão ``4.12.2``, também foi utilizada.

As dependências do projeto estão listadas no arquivo `requirements.txt`.

### 🤖 Executando o crawler

Para executar o projeto, siga estas etapas:

1. Após baixar o projeto, abra um terminal dentro da pasta raiz (``crawler-jusbrasil-challenge``), execute o comando
   abaixo para instalar as dependências utilizando
   o `pip`:

````shell
pip install -r requirements.txt
````

2. Depois que as dependências forem instaladas, ainda no terminal, execute o comando a seguir:

```
python main.py
```

3. Pronto! Seus dados estarão salvos no arquivo `result.json`, dentro do diretório ``docs`` (não se preocupe: caso o
   diretório ou o arquivo ainda não existam, eles serão criados na primeira vez que executar o programa). Abaixo está um
   exemplo do JSON salvo:

```json
[
  {
    "_dataExtracao": "2023-06-29 13:02:30.988729",
    "_dataJulgamentoValida": true,
    "_dataPublicacaoValida": true,
    "_id": 1,
    "assunto": "Apelação Cível / Bancários",
    "comarca": "Santa Fé do Sul",
    "dataJulgamento": "26/01/2022",
    "dataPublicacao": "26/01/2022",
    "ementa": "RESPONSABILIDADE CIVIL – Ação declaratória de inexigibilidade de débito c.c. indenização por dano moral – Contratação não reconhecida pelo autor – Origem do débito não comprovada – Falha na prestação do serviço – Responsabilidade objetiva da prestadora de serviços – Risco profissional – Dano moral bem caracterizado – Indenização arbitrada segundo o critério da prudência e razoabilidade",
    "numeroProcesso": "1001143-04.2021.8.26.0541",
    "orgaoJulgador": "20ª Câmara de Direito Privado",
    "relator": "Correia Lima"
  },
  {
    ...
  }
]
```

---

## ❗ Informações complementares

> Nesta seção estão respondidas demais informações solicitadas junto com a resolução do desafio.

### 📆 Prazos:

- **Data de início:** ``22/06/2023``
- **Data de conclusão:** ``26/06/2023``
- **Data de submissão:** ``29/06/2023``

### ⏰ Tempo investido:

<img src="assets/forest_tempdev.png " alt="Gráfico com tempo utilizado para desenvolvimento" width="350" height="350">

- **Tempo para desenvolver os requisitos mínimos da aplicação:** ``7 horas e 20 min``

<img src="assets/forest_temptotal.jpg " alt="Gráfico com tempo utilizado para desenvolvimento" width="350" height="350">

- **Tempo total (incluindo documentação, refinamentos e melhorias):** ``10 horas e 24 min``

---

### 🔨 Requisitos básicos, ajustes e melhorias

> O que você não incluiu em sua solução que gostaria que soubéssemos: Você estava com pouco tempo e não conseguiu
> incluir algo?
> Outras informações sobre sua solução que você acha que seria importante sabermos (se aplicável).

**Requisitos básicos:**

- [x] Extrair dados
- [x] Salvar dados extraídos em um único arquivo JSON
- [x] Escrever ``README.md``

**Ajustes e melhorias:**

- [x] Melhorar tratamento dos dados
- [x] Enriquecer dados
    - [x] Validação do formato de datas
    - [x] Adicionar informação de quando a extração foi feita
- [x] Tratamento de exceções
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
   representa um índice, e de outras tabelas, onde estão localizadas as informações das jurisprudências. Nessas
   tags `table` mais internas, pude notar que todas as informações que precisaria extrarir estavam dentro de uma "
   etiquetas" (**Ementa:**, **Classe / Assunto:**, etc.). Logo, poderia utilizar esse padrão para extrair a
   informação. Nesse ponto havia outros dois possíveis caminhos:
    1. Navegar pelo HTML até o nível da ``<div id="divDadosResultado-A">``, localizar a tabela agregadora das demais
       tags `<table>`, percorrer as tags `tr` dessas tabelas internas e então utilizar Expressões Regulares a fim
       de identificar o padrão dessas "etiquetas" e considerar os textos após essas; ou
    2. Se não fossem essas "etiquetas", seria necessário identificar algum outro padrão a nível de _tag_ para que,
       usando o BeautilfulSoup, pudesse atingir as informações.

Optei pela opção ii, uma vez as _tags_ mais internas das tabelas que continham os dados de jurisprudência não seguiam
um padrão muito bem definido, tornando a opção ii um pouco mais inviável para o objetivo.

As informações de data me pareceram relevantes. Portanto, julguei que seria interessante realizar uma validação sobre
elas. Para isso, no arquivo JSON, cada objeto que representa uma jurisprudência possui os atributos ``dataPublicacao``
e ``dataJulgamento``. Como essas informações são obtidas como strings durante a extração, criei uma função responsável
por verificá-las a fim de saber se tratam de datas válidas ou não, armazenando esta informação em atributos extras,
nomeados de ``_dataPublicacaoValida`` e ``_dataJulgamentoValida``, respectivamente.

Essa abordagem me levou a criar um outro atributo para ser armazenado junto com a juriprudência extraída: a data em que
a extração foi feita. Por isso, também acrescentei o atributo ``_dataExtracao`` aos objetos antes de serem salvos no
arquivo JSON.

### 🔀 Atalhos realizados:

> Se aplicável, você fez algo que sentiu que poderia ter feito melhor em uma aplicação do "mundo real"?

Como neste cenário existia esse padrão das "etiquetas", preferi adotar essa estratégia, conforme explicado acima. Porém,
algumas vezes me questionei se num cenário do "mundo real" o ideal seria não depender desses padrões textuais e fosse
preferível fazer um crawler que navegasse a nível de estrutura de página.

Além disso, estamos considerando um cenário no qual o crawler "varre" uma única página. Em uma aplicação do "mundo real"
seria importante que o crawler fosse capaz de navegar entre outras páginas, procurando outras informações de
jurisprudência. Porém, não _ao infinito e além_, mas por tempo o suficiente para que pudesse percorrer as páginas que
continham essas informações.

Para este cenário também não me preocupei com a sobrecarga que o crawler poderia gerar. Mas, acredito que numa
aplicação "real" isso deve ser um ponto relevante.

Por fim, o crawler desenvolvido não é tolerante à falhas; apesar de haver tratamento de exeção ou outro.

### 💬 Feedbacks:

> Você tem algum feedback para tornarmos esse desafio melhor? Por favor, nos conte. :)

Até que me diverti fazendo o desafio. Achei tanto o objetivos quanto as orientações bem claras. Então, mesmo estando em
semana de avaliações de final de semestre na faculdade, isso me ajudou entender o que deveria ser feito.

Além disso, aproveitei a oportunidade para iniciar a leitura do
livro [Web Scraping com Python](https://www.amazon.com.br/Web-Scraping-Com-Python-Coletando/dp/8575227300/ref=sr_1_8?__mk_pt_BR=%C3%85M%C3%85%C5%BD%C3%95%C3%91&crid=3LL9RB4MO701K&keywords=python&qid=1687927515&sprefix=pytho%2Caps%2C232&sr=8-8),
que havia comprado há um tempinho atrás. Fui aprendendo algumas coisas no caminho e foi interessante ver que consegui
aplicar num desafio prático. Esse desafio também acabou me permitindo experimentar algumas coisas pela primeira vez,
como foi o caso das expressões regulares.

[⬆ Voltar ao topo](#jusbrasil-crawler-challenge)<br>

