# Criação e Configuração de Máquina Virtual no Microsoft Azure

## 📋 Pré-requisitos

- Conta ativa no Microsoft Azure
- Assinatura válida do Azure (gratuita ou paga)
- Acesso ao Portal do Azure (portal.azure.com)

## 🚀 Processo de Criação da VM

### Passo 1: Acessar o Portal do Azure

1. Acesse [portal.azure.com](https://portal.azure.com)
2. Faça login com suas credenciais Microsoft
3. No painel principal, localize o botão **"Criar um recurso"** (ícone de "+")

*Visualização: Painel principal do Azure com menu lateral esquerdo e botão azul "Criar um recurso" no topo*

### Passo 2: Selecionar Máquina Virtual

1. Na página "Criar um recurso", clique em **"Máquina Virtual"**
2. Alternativamente, use a barra de pesquisa e digite "Virtual Machine"
3. Clique em **"Criar"** → **"Máquina virtual do Azure"**

*Visualização: Página de recursos com categorias como "Computação", "Rede", "Armazenamento". VM aparece destacada na seção Computação*

### Passo 3: Configurações Básicas

#### 3.1 Detalhes do Projeto
- **Assinatura**: Selecione sua assinatura ativa
- **Grupo de recursos**: 
  - Criar novo: Digite um nome (ex: `rg-vm-teste`)
  - Ou selecionar existente

#### 3.2 Detalhes da Instância
- **Nome da máquina virtual**: `vm-exemplo-01`
- **Região**: Escolha a mais próxima (ex: `Brazil South`)
- **Opções de disponibilidade**: 
  - Para testes: "Nenhuma redundância de infraestrutura necessária"
  - Para produção: "Conjunto de disponibilidade" ou "Zona de disponibilidade"

#### 3.3 Imagem e Tamanho
- **Imagem**: 
  - Windows: `Windows Server 2022 Datacenter`
  - Linux: `Ubuntu Server 20.04 LTS`
- **Tamanho**: 
  - Para testes: `Standard_B1s` (1 vCPU, 1GB RAM)
  - Para desenvolvimento: `Standard_B2s` (2 vCPUs, 4GB RAM)

*Visualização: Formulário com campos de seleção dropdown e campos de texto. Seção "Tamanho" mostra tabela com diferentes configurações de CPU/RAM*

#### 3.4 Conta de Administrador

**Para Windows:**
- **Nome de usuário**: `azureuser`
- **Senha**: Senha forte (mín. 12 caracteres)
- **Confirmar senha**: Repetir a senha

**Para Linux:**
- **Tipo de autenticação**: 
  - Senha: Configure usuário e senha
  - Chave SSH: Upload da chave pública

#### 3.5 Regras de Porta de Entrada
- Marque: **"Permitir portas selecionadas"**
- **Portas de entrada públicas**:
  - Windows: `RDP (3389)`
  - Linux: `SSH (22)`, `HTTP (80)`, `HTTPS (443)`

### Passo 4: Configurações de Discos

1. Clique em **"Próximo: Discos"**
2. **Tipo de disco do SO**: 
   - Desenvolvimento: `SSD Standard`
   - Produção: `SSD Premium`
3. **Criptografia**: Manter padrão (habilitado)
4. Para discos adicionais: Clique em **"Criar e anexar um novo disco"**

*Visualização: Interface com opções de tipo de disco em cards visuais mostrando SSD Premium, SSD Standard, e HDD Standard com preços*

### Passo 5: Configurações de Rede

1. **Rede virtual**: Criar nova ou usar existente
   - Nome: `vnet-vm-exemplo`
   - Espaço de endereço: `10.0.0.0/16`
2. **Sub-rede**: 
   - Nome: `subnet-default`
   - Intervalo: `10.0.0.0/24`
3. **IP público**: Criar novo
   - Nome: `ip-vm-exemplo`
   - SKU: `Standard`
4. **Grupo de segurança de rede**: Básico
5. **Balanceamento de carga**: Não (para VM única)

### Passo 6: Gerenciamento

Configurações recomendadas:
- **Identidade**: Habilitada (identidade gerenciada atribuída pelo sistema)
- **Logon do Azure AD**: Habilitado (para Windows)
- **Desligamento automático**: 
  - Habilitado: `19:00` (para economizar custos)
  - Fuso horário: `(UTC-03:00) Brasília`
- **Backup**: 
  - Habilitado para produção
  - Desabilitado para testes

### Passo 7: Monitoramento

- **Diagnóstico de inicialização**: Habilitado
- **Diagnósticos do SO convidado**: Habilitado
- **Insights da VM**: Habilitado (recomendado)

### Passo 8: Configurações Avançadas

Geralmente manter padrões, exceto:
- **Extensões**: Adicionar se necessário (ex: antivírus, agents)
- **Dados personalizados**: Scripts de inicialização (se aplicável)

### Passo 9: Tags (Opcional)

Adicionar tags para organização:
- `Ambiente`: `Desenvolvimento`
- `Projeto`: `NomeDoProjeto`
- `Responsável`: `SeuNome`

### Passo 10: Revisar e Criar

1. Clique em **"Revisar + criar"**
2. Aguarde a validação (barra verde de progresso)
3. Revise o resumo e custos estimados
4. Clique em **"Criar"**

*Visualização: Página de resumo com todas as configurações em formato de lista, custos mensais estimados em destaque, e botão azul "Criar"*

## 🔧 Pós-Criação: Configuração Inicial

### Conexão com a VM

#### Windows (RDP)
```bash
# No portal Azure, vá para a VM → Conectar → RDP
# Baixe o arquivo .rdp e execute
# Use as credenciais configuradas
```

#### Linux (SSH)
```bash
# Obtenha o IP público da VM no portal
ssh azureuser@<IP_PUBLICO>
```

### Configurações de Segurança Recomendadas

#### 1. Atualização do Sistema
**Windows:**
```powershell
# Execute Windows Update
Get-WindowsUpdate -Install -AcceptAll
```

**Linux:**
```bash
sudo apt update && sudo apt upgrade -y
```

#### 2. Configuração de Firewall
**Windows:**
- Configure Windows Defender Firewall
- Libere apenas portas necessárias

**Linux (Ubuntu):**
```bash
sudo ufw enable
sudo ufw allow ssh
sudo ufw allow http
sudo ufw allow https
```

#### 3. Grupos de Segurança de Rede (NSG)
No portal Azure:
1. Vá para a VM → Rede
2. Clique no NSG associado
3. Configure regras específicas:
   - Remova regras muito permissivas
   - Adicione regras por IP de origem específico

## 💰 Gerenciamento de Custos

### Estratégias de Economia
1. **Desligamento automático**: Configure horários
2. **Dimensionamento adequado**: Monitore uso de CPU/RAM
3. **Reservas**: Para VMs de longa duração
4. **Discos**: Use SSD Standard para desenvolvimento

### Monitoramento de Custos
```bash
# No portal: Serviços → Gerenciamento de Custos + Cobrança
# Configure alertas de orçamento
# Analise relatórios de uso
```

## 🔍 Monitoramento e Manutenção

### Métricas Importantes
- **CPU**: < 80% em média
- **Memória**: < 85% utilização
- **Disco**: < 90% de uso
- **Rede**: Monitorar throughput

### Azure Monitor
1. Habilite Application Insights
2. Configure alertas personalizados
3. Analise logs regularmente

## ❌ Problemas Comuns e Soluções

### 1. Não consegue conectar via RDP/SSH
**Solução:**
- Verifique NSG (porta liberada)
- Confirme IP público atribuído
- Teste conectividade de rede

### 2. VM lenta ou travando
**Solução:**
- Verifique métricas de CPU/RAM
- Considere upgrade de tamanho
- Analise processos em execução

### 3. Custos elevados
**Solução:**
- Configure desligamento automático
- Redimensione a VM
- Analise discos desnecessários

## 📚 Recursos Úteis

- [Documentação Oficial Azure VM](https://docs.microsoft.com/azure/virtual-machines/)
- [Calculadora de Preços Azure](https://azure.microsoft.com/pricing/calculator/)
- [Azure Advisor](https://portal.azure.com/#blade/Microsoft_Azure_Expert/AdvisorMenuBlade/overview)
- [Azure Status](https://status.azure.com/)

## 🏷️ Tags Sugeridas para Organização

| Tag | Exemplo | Descrição |
|-----|---------|-----------|
| Environment | Production/Development | Ambiente da VM |
| Project | WebApp-Frontend | Projeto relacionado |
| Owner | joao.silva@empresa.com | Responsável |
| CostCenter | TI-001 | Centro de custo |
| AutoShutdown | Enabled | Controle de desligamento |

---

**💡 Dica Final:** Sempre inicie com configurações básicas e dimensione conforme necessário. O Azure permite ajustes posteriores na maioria das configurações.

**⚠️ Importante:** Lembre-se de desligar VMs não utilizadas para evitar custos desnecessários!