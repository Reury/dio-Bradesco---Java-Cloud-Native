# Configuração e Dimensionamento de Máquinas Virtuais no Microsoft Azure

Este documento resume os principais conceitos explorados no laboratório do módulo de Computação e Rede na Azure, com foco na criação, configuração e dimensionamento de **Máquinas Virtuais (VMs)**.

## 📌 Introdução

O laboratório apresenta um panorama prático da computação na nuvem utilizando o Microsoft Azure, com ênfase na criação e gestão de Máquinas Virtuais (VMs). Também são abordadas instâncias de contêineres, serviços web e áreas de trabalho virtuais.

---

## ⚙️ Criação de Máquinas Virtuais

### Passo a passo básico:
1. Acesse o portal do Microsoft Azure.
2. Vá até **"Máquina Virtual"** no menu principal.
3. Escolha a opção de criar uma VM com:
   - Configuração pré-definida
   - VMs e soluções relacionadas

> 💡 **Dica**: Existem templates e padrões disponíveis para facilitar a criação de VMs com configurações comuns.

---

## 🛠️ Configuração de Recursos

Durante a criação de uma VM, você poderá configurar:

- **Sistema Operacional**: Windows, Linux (Ubuntu, CentOS etc.)
- **Tamanho da Máquina (SKU)**:
  - CPU, RAM, disco
  - Exemplo: Standard_B2s, D2s_v3 etc.
- **Região de hospedagem**
- **Disco do SO e discos de dados adicionais**
- **Grupos de recursos**: facilitam o gerenciamento conjunto de recursos

---

## 📏 Dimensionamento de Recursos

Você pode dimensionar a VM conforme a carga de trabalho:

- **Vertical**: aumentar CPU/RAM (mudar o SKU da VM)
- **Horizontal**: usar escalabilidade automática com múltiplas instâncias

> 🔁 O **AutoScale** pode ser configurado com base em métricas como uso de CPU, memória ou número de requisições.

---

## 🔐 Segurança e Acesso

- **Usuário e senha SSH/administrador**
- **Regras de grupo de segurança de rede (NSG)**:
  - Abertura de portas (RDP, SSH, HTTP, etc.)
- **IP público e DNS configuráveis**

---

## 🧪 Dicas do Laboratório

- As opções de VMs pré-configuradas são úteis para testes rápidos.
- Explore os "modelos ARM" para automação da criação.
- Fique atento às práticas recomendadas para otimizar custo e desempenho.

---

## 🚀 Considerações Finais

O uso de Máquinas Virtuais na Azure é uma das formas mais versáteis de implementar cargas de trabalho. Saber dimensionar e configurar corretamente garante melhor desempenho, economia e segurança para seus projetos em nuvem.

---
