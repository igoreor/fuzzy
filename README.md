# 🎤 Sistema de Avaliação de Apresentações com Lógica Fuzzy

## 📋 Sobre o Projeto

Sistema inteligente desenvolvido com **Lógica Fuzzy** para avaliar apresentações orais de forma objetiva e construtiva. O sistema transforma avaliações subjetivas em notas quantitativas e fornece feedback personalizado para melhoria.

### 🎯 Objetivos

- Construir um modelo de inferência fuzzy que combine múltiplos critérios de avaliação
- Gerar uma nota final interpretável em termos linguísticos amigáveis
- Fornecer feedback construtivo e sugestões de melhoria
- Demonstrar aplicação prática da lógica fuzzy em IA

---

## 🧠 O que é Lógica Fuzzy?

A lógica fuzzy (ou lógica difusa) trabalha com **graus de verdade** entre 0 e 1, permitindo representar incertezas e informações imprecisas — algo mais próximo do raciocínio humano.

**Exemplo:** "A apresentação foi clara" pode ter valor 0.3, 0.7, 0.95, etc., dependendo da intensidade da clareza, ao invés de apenas "sim" ou "não".

### 🔧 Aplicações
- Controles de temperatura de ar-condicionado
- Máquinas de lavar inteligentes
- Direção automática
- Inteligência artificial
- **Avaliação de apresentações** ← Nosso projeto!

---

## 📊 Variáveis do Sistema

### Variáveis de Entrada (0-10)

1. **Clareza** - Quão clara foi a explicação do conteúdo
   - Baixa (0-4) | Média (2-8) | Alta (6-10)

2. **Domínio** - Conhecimento demonstrado sobre o assunto
   - Fraco (0-4) | Médio (2-8) | Forte (6-10)

3. **Ritmo** - Velocidade e fluidez da fala
   - Devagar (0-4) | Adequado (3-7) | Rápido (6-10)

4. **Materiais** - Qualidade dos slides e recursos visuais
   - Ruins (0-4) | Aceitáveis (2-8) | Bons (6-10)

5. **Engajamento** - Interação com a plateia, contato visual
   - Baixo (0-4) | Médio (2-8) | Alto (6-10)

### Variável de Saída (0-10)

**Avaliação Final** com 5 classificações:
- 🔴 **Precisa Melhorar** (0-3)
- 🟡 **Aceitável** (3-5)
- 🟢 **Bom** (5-7)
- 🔵 **Muito Bom** (7-8.5)
- 🟣 **Excelente** (8.5-10)

---

## 📝 Base de Regras Fuzzy

O sistema utiliza **15 regras** de inferência (formato IF-THEN):

### Exemplos de Regras:

1. **IF** Clareza=Alta **AND** Domínio=Forte **AND** Engajamento=Alto **THEN** Avaliação=Excelente
2. **IF** Clareza=Baixa **AND** Domínio=Fraco **THEN** Avaliação=Precisa Melhorar
3. **IF** Ritmo=Devagar **OR** Ritmo=Rápido **AND** Engajamento=Baixo **THEN** Avaliação=Aceitável
4. **IF** Materiais=Bons **AND** Clareza=Média **AND** Domínio=Médio **THEN** Avaliação=Bom
5. **IF** Engajamento=Alto **AND** Ritmo=Adequado **THEN** Avaliação=Muito Bom

... e mais 10 regras complementares!

### Método de Inferência

- **Tipo:** Mamdani (clássico)
- **Agregação:** max (OR) e min (AND)
- **Defuzzificação:** Centro de gravidade (centroid)

---

## 🚀 Como Usar

### Opção 1: Usando Docker (Recomendado)

```bash
# Clone ou baixe o repositório
cd fuzzy

# Construa e execute o container
docker-compose up

# Ou usando apenas Docker
docker build -t fuzzy-app .
docker run -p 8501:8501 fuzzy-app
```

A interface web estará disponível em `http://localhost:8501`

**Vantagens do Docker:**
- ✅ Não precisa instalar dependências manualmente
- ✅ Ambiente isolado e reproduzível
- ✅ Funciona em qualquer sistema operacional
- ✅ Sem conflitos de versões

### Opção 2: Instalação Local

```bash
# Clone ou baixe o repositório
cd fuzzy

# Crie um ambiente virtual (opcional mas recomendado)
python -m venv venv
.\venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Instale as dependências
pip install -r requirements.txt

# Execute o Streamlit
streamlit run app.py
```

A interface web será aberta no navegador automaticamente em `http://localhost:8501`

### Uso do Sistema Python

```python
from fuzzy_system import AvaliacaoApresentacaoFuzzy

# Cria o sistema
sistema = AvaliacaoApresentacaoFuzzy()

# Avalia uma apresentação
resultado = sistema.avaliar(
    clareza_val=7.5,
    dominio_val=8.0,
    ritmo_val=6.0,
    materiais_val=7.0,
    engajamento_val=8.5
)

print(f"Nota: {resultado['nota']}/10")
print(f"Classificação: {resultado['classificacao']}")
print(f"Feedback: {resultado['feedback']}")
```

### Notebook Google Colab

Abra o arquivo [avaliacao_fuzzy_colab.ipynb](avaliacao_fuzzy_colab.ipynb) no Google Colab para:
- Ver explicações detalhadas
- Executar 12+ exemplos de teste
- Visualizar gráficos das funções de pertinência
- Fazer testes interativos

---

## 📁 Estrutura do Projeto

```
fuzzy/
├── README.md                      # Documentação principal
├── requirements.txt               # Dependências do projeto
├── Dockerfile                     # Configuração Docker
├── docker-compose.yml             # Orquestração Docker
├── .dockerignore                  # Arquivos ignorados pelo Docker
├── fuzzy_system.py               # Sistema fuzzy (núcleo)
├── app.py                        # Interface Streamlit
└── avaliacao_fuzzy_colab.ipynb   # Notebook para Google Colab
```

---

## 🧪 Exemplos de Teste

O sistema foi testado com 12+ cenários diferentes:

| Cenário | Clareza | Domínio | Ritmo | Materiais | Engajamento | Nota | Classificação |
|---------|---------|---------|-------|-----------|-------------|------|---------------|
| Apresentação Excelente | 9.0 | 9.5 | 6.0 | 8.5 | 9.0 | ~9.0 | Excelente |
| Muito Boa (Materiais Simples) | 8.0 | 8.5 | 5.5 | 6.0 | 8.0 | ~7.8 | Muito Bom |
| Boa Apresentação Geral | 7.0 | 7.0 | 6.0 | 7.0 | 6.5 | ~6.8 | Bom |
| Aceitável (Baixo Engajamento) | 5.0 | 6.0 | 5.0 | 5.0 | 3.0 | ~4.5 | Aceitável |
| Precisa Melhorar | 2.0 | 3.0 | 4.0 | 2.5 | 2.0 | ~2.5 | Precisa Melhorar |

*(Veja todos os testes no notebook Colab ou execute a interface Streamlit)*

---

## 💡 Recursos da Interface Web

- ✅ Sliders interativos para cada critério (0-10)
- ✅ Avaliação em tempo real
- ✅ Gráfico radar com análise dos critérios
- ✅ Feedback construtivo e sugestões de melhoria
- ✅ Visualização das funções de pertinência
- ✅ Modo de teste automático com 12 cenários
- ✅ Estatísticas e comparações

---

## 🔬 Justificativa Técnica

### Por que Lógica Fuzzy?

A avaliação de apresentações é **intrinsecamente subjetiva e imprecisa**, tornando-a um caso ideal para lógica fuzzy:

1. **Subjetividade**: "Bom domínio" significa coisas diferentes para diferentes avaliadores
2. **Gradação**: Uma apresentação pode ser "parcialmente clara" ou "muito boa"
3. **Múltiplos critérios**: Combinar clareza, ritmo, engajamento, etc. requer inferência complexa
4. **Raciocínio humano**: A lógica fuzzy imita como humanos pensam sobre qualidade

### Vantagens do Sistema

- ✅ Reduz viés individual do avaliador
- ✅ Fornece critérios objetivos e consistentes
- ✅ Gera feedback construtivo automaticamente
- ✅ Transparência (regras claras e interpretáveis)
- ✅ Pode ser calibrado com dados reais

---

## 📚 Tecnologias Utilizadas

- **Python 3.8+**
- **scikit-fuzzy** - Biblioteca de lógica fuzzy
- **Streamlit** - Interface web interativa
- **Matplotlib** - Visualização de gráficos
- **Plotly** - Gráficos interativos
- **NumPy** - Computação numérica
- **Pandas** - Manipulação de dados

---

## 🎓 Conceitos Demonstrados

### Componentes da Lógica Fuzzy

1. **Fuzzificação** - Conversão de valores precisos (ex: 7.5) em graus de pertinência
2. **Base de Regras** - 15 regras IF-THEN que capturam conhecimento especializado
3. **Inferência** - Método Mamdani para combinar regras
4. **Defuzzificação** - Centro de gravidade para gerar nota final

### Funções de Pertinência

Utilizamos **funções triangulares** (trimf) por:
- Simplicidade de interpretação
- Eficiência computacional
- Adequação ao problema

---

## 🔮 Possíveis Extensões

1. **Reconhecimento automático** - Integração com análise de áudio/vídeo
2. **Aprendizado de regras** - Usar algoritmos genéticos ou ANFIS para otimizar regras
3. **Feedback em linguagem natural** - Gerar frases mais detalhadas com NLP
4. **Avaliação por pares** - Sistema colaborativo com múltiplos avaliadores
5. **Histórico e progresso** - Acompanhamento da evolução ao longo do tempo

---

## 📊 Calibração e Validação

### Métricas de Avaliação Sugeridas

- **Consistência**: MAE (Mean Absolute Error) entre sistema fuzzy e média humana
- **Concordância**: Correlação de Spearman/Pearson
- **Feedback qualitativo**: Validação com usuários reais

### Como Calibrar

1. Coletar 20-30 avaliações de apresentações reais
2. Comparar notas do sistema com médias humanas
3. Ajustar funções de pertinência e regras
4. Iterar até alcançar consistência desejada

---

## 👥 Contribuindo

Este é um projeto educacional. Sugestões de melhoria:

- Adicionar mais critérios de avaliação
- Refinar regras baseadas em dados reais
- Implementar novas funcionalidades na interface
- Criar mais exemplos de teste

---

## 📄 Licença

Este projeto foi desenvolvido para fins educacionais como parte de um trabalho acadêmico de Inteligência Artificial.

---

## 🎯 Conclusão

Este projeto demonstra com sucesso a aplicação prática da **Lógica Fuzzy** em um problema real e relevante: a avaliação de apresentações orais.

O sistema:
- ✅ Define claramente variáveis de entrada e saída
- ✅ Implementa funções de pertinência interpretáveis
- ✅ Utiliza 15 regras fuzzy bem fundamentadas
- ✅ Foi testado com 12+ cenários diferentes
- ✅ Fornece interface amigável e visualizações

A lógica fuzzy se mostrou adequada para lidar com a **subjetividade** e **imprecisão** inerentes à avaliação de apresentações, gerando resultados coerentes e feedback útil.

---

## 📞 Contato e Suporte

Para dúvidas sobre o projeto, consulte:
- O notebook Colab com explicações detalhadas
- Os comentários no código-fonte
- A documentação das bibliotecas utilizadas

---

**Desenvolvido com ❤️ usando Python e Lógica Fuzzy**

*Projeto de Inteligência Artificial - Sistema de Avaliação de Apresentações*
