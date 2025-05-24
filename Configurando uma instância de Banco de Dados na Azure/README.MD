# Guia de Configuração de Banco de Dados no Microsoft Azure

## 📋 Objetivo

Este repositório contém um guia prático para configuração de instâncias de Banco de Dados na plataforma Microsoft Azure, servindo como material de apoio para estudos e implementações futuras.

## 🎯 Público-Alvo

- Desenvolvedores iniciantes em cloud computing
- Profissionais migrando para Azure
- Estudantes de tecnologia da informação
- Arquitetos de soluções em formação

## 📚 Índice

1. [Introdução ao Azure Database](#introdução-ao-azure-database)
2. [Tipos de Banco de Dados Disponíveis](#tipos-de-banco-de-dados-disponíveis)
3. [Pré-requisitos](#pré-requisitos)
4. [Configuração Passo a Passo](#configuração-passo-a-passo)
5. [Configurações de Segurança](#configurações-de-segurança)
6. [Monitoramento e Performance](#monitoramento-e-performance)
7. [Backup e Recuperação](#backup-e-recuperação)
8. [Custos e Otimização](#custos-e-otimização)
9. [Dicas e Boas Práticas](#dicas-e-boas-práticas)
10. [Troubleshooting](#troubleshooting)
11. [Recursos Adicionais](#recursos-adicionais)

## 🌟 Introdução ao Azure Database

O Microsoft Azure oferece diversos serviços de banco de dados gerenciados que eliminam a necessidade de configurar e manter a infraestrutura subjacente. Os principais benefícios incluem:

- **Alta Disponibilidade**: SLA de até 99,99%
- **Escalabilidade Automática**: Ajuste de recursos conforme demanda
- **Segurança Integrada**: Criptografia, firewall e autenticação
- **Backup Automático**: Proteção contra perda de dados
- **Monitoramento**: Insights de performance em tempo real

## 🗄️ Tipos de Banco de Dados Disponíveis

### SQL Database (PaaS)
- **Descrição**: Banco de dados SQL Server totalmente gerenciado
- **Ideal para**: Aplicações modernas que precisam de recursos SQL avançados
- **Características**: Escalabilidade automática, inteligência integrada

### MySQL Database
- **Descrição**: MySQL totalmente gerenciado
- **Ideal para**: Aplicações web, e-commerce
- **Características**: Compatibilidade total com MySQL Community

### PostgreSQL Database
- **Descrição**: PostgreSQL totalmente gerenciado
- **Ideal para**: Aplicações que requerem recursos avançados de banco relacional
- **Características**: Suporte a JSON, extensões personalizadas

### Cosmos DB
- **Descrição**: Banco NoSQL multi-modelo
- **Ideal para**: Aplicações globalmente distribuídas
- **Características**: Baixa latência, múltiplos modelos de dados

### SQL Managed Instance
- **Descrição**: SQL Server com compatibilidade quase 100%
- **Ideal para**: Migração lift-and-shift de SQL Server on-premises
- **Características**: Instância dedicada, recursos avançados

## ⚡ Pré-requisitos

### Conta Azure
- Conta ativa do Microsoft Azure
- Créditos disponíveis ou assinatura válida
- Permissões adequadas (Contributor ou Owner role)

### Ferramentas Necessárias
- Navegador web atualizado
- Azure CLI (opcional)
- Azure PowerShell (opcional)
- Cliente de banco de dados (SQL Server Management Studio, MySQL Workbench, etc.)

### Conhecimentos Básicos
- Conceitos de banco de dados relacionais
- Noções básicas de redes e segurança
- Fundamentos de cloud computing

## 🔧 Configuração Passo a Passo

### Passo 1: Acessar o Portal Azure
1. Acesse [portal.azure.com](https://portal.azure.com)
2. Faça login com suas credenciais
3. No painel principal, clique em "Criar um recurso"

### Passo 2: Selecionar o Tipo de Banco
1. Na categoria "Bancos de dados", escolha o tipo desejado
2. Clique em "Criar" no serviço selecionado
3. Selecione o modelo de implantação (se aplicável)

### Passo 3: Configurações Básicas
```
Assinatura: [Sua assinatura ativa]
Grupo de recursos: [Criar novo ou usar existente]
Nome do servidor: [nome-unico-servidor]
Região: [Região mais próxima dos usuários]
Método de autenticação: [SQL Authentication ou Azure AD]
Login do administrador: [nome-admin]
Senha: [senha-forte-12-caracteres]
```

### Passo 4: Configurações de Compute e Storage
```
Nível de serviço: 
- Basic: Para desenvolvimento e teste
- Standard: Para cargas de trabalho pequenas a médias
- Premium: Para cargas de trabalho críticas

Tamanho do compute: [Baseado na necessidade]
Armazenamento: [GB necessários]
Backup: [Período de retenção]
```

### Passo 5: Configurações de Rede
```
Conectividade: 
- Endpoint público: Acesso via internet
- Endpoint privado: Acesso apenas via VNet

Regras de firewall:
- Permitir acesso de serviços Azure: Sim/Não
- Adicionar IP do cliente atual: Sim/Não
- Regras personalizadas: [IPs específicos]
```

### Passo 6: Configurações Adicionais
```
Origem dos dados:
- Banco vazio
- Exemplo (AdventureWorks)
- Backup existente

Agrupamento: SQL_Latin1_General_CP1_CI_AS (padrão)
Proteção Avançada contra Ameaças: Habilitado
```

### Passo 7: Revisão e Criação
1. Revise todas as configurações
2. Verifique estimativa de custos
3. Clique em "Criar"
4. Aguarde a implantação (5-10 minutos)

## 🔒 Configurações de Segurança

### Firewall do Servidor
```sql
-- Configurar regras de firewall via T-SQL
EXEC sp_set_firewall_rule 
    @name = 'AllowMyIP', 
    @start_ip_address = '192.168.1.1', 
    @end_ip_address = '192.168.1.1';
```

### Transparent Data Encryption (TDE)
- **Habilitado por padrão** em SQL Database
- Criptografia automática dos dados em repouso
- Chaves gerenciadas pelo serviço ou pelo cliente

### Always Encrypted
```sql
-- Exemplo de configuração Always Encrypted
CREATE COLUMN MASTER KEY [CMK1]
WITH (
    KEY_STORE_PROVIDER_NAME = 'AZURE_KEY_VAULT',
    KEY_PATH = 'https://myvault.vault.azure.net/keys/mykey/key-id'
);
```

### Azure Active Directory Integration
```powershell
# Configurar admin do Azure AD
Set-AzSqlServerActiveDirectoryAdministrator 
    -ResourceGroupName "myResourceGroup" 
    -ServerName "myServer" 
    -DisplayName "DBA Group"
```

## 📊 Monitoramento e Performance

### Métricas Importantes
- **DTU/vCore Utilization**: Uso de recursos de compute
- **Storage Usage**: Espaço em disco utilizado
- **Connection Count**: Número de conexões ativas
- **Deadlocks**: Travamentos de transações
- **Query Performance**: Tempo de resposta das consultas

### Query Performance Insight
1. Acesse o recurso no portal Azure
2. Navegue para "Query Performance Insight"
3. Analise as consultas mais demoradas
4. Implemente otimizações sugeridas

### Alertas Personalizados
```json
{
    "name": "High DTU Usage",
    "description": "Alert when DTU usage exceeds 80%",
    "condition": {
        "metric": "dtu_consumption_percent",
        "operator": "GreaterThan",
        "threshold": 80
    },
    "action": {
        "type": "email",
        "recipients": ["admin@company.com"]
    }
}
```

## 💾 Backup e Recuperação

### Backup Automático
- **Backup completo**: Semanal
- **Backup diferencial**: A cada 12-24 horas
- **Backup de log de transações**: A cada 5-10 minutos
- **Retenção**: 7-35 dias (configurável)

### Restauração Point-in-Time
```powershell
# Restaurar banco para um ponto específico no tempo
Restore-AzSqlDatabase 
    -FromPointInTimeBackup 
    -PointInTime "2024-01-15T10:30:00Z" 
    -ResourceGroupName "myResourceGroup" 
    -ServerName "myServer" 
    -TargetDatabaseName "myDatabase-restored" 
    -ResourceId "/subscriptions/.../databases/myDatabase"
```

### Geo-Replication
```sql
-- Configurar replica secundária
ALTER DATABASE [myDatabase] 
ADD SECONDARY ON SERVER [secondary-server] 
WITH (ALLOW_CONNECTIONS = ALL);
```

## 💰 Custos e Otimização

### Modelos de Preços

#### DTU Model
- **Basic**: R$ 15-50/mês
- **Standard**: R$ 50-500/mês  
- **Premium**: R$ 500-3000/mês

#### vCore Model
- **General Purpose**: R$ 200-1000/mês
- **Business Critical**: R$ 800-4000/mês
- **Hyperscale**: Variável conforme uso

### Dicas de Otimização de Custos
1. **Right-sizing**: Monitore uso e ajuste recursos
2. **Reserved Instances**: Economize até 55% com reservas
3. **Pause/Resume**: Para ambientes de desenvolvimento
4. **Elastic Pools**: Compartilhe recursos entre bancos
5. **Cleanup**: Remova recursos não utilizados

### Calculadora de Custos
Use a [Calculadora de Preços do Azure](https://azure.microsoft.com/pricing/calculator/) para estimar custos antes da implementação.

## 💡 Dicas e Boas Práticas

### Nomenclatura
```
Convenção sugerida:
- Servidor: srv-[projeto]-[ambiente]-[região]
- Banco: db-[aplicacao]-[ambiente]
- Exemplo: srv-ecommerce-prod-eastus
```

### Performance
1. **Indexação adequada**: Monitore missing indexes
2. **Estatísticas atualizadas**: Configure auto-update
3. **Query tuning**: Use Query Store para análise
4. **Connection pooling**: Configure no lado da aplicação

### Segurança
1. **Princípio do menor privilégio**: Conceda apenas permissões necessárias
2. **Rotação de senhas**: Implemente política de rotação
3. **Auditoria**: Habilite logging de atividades críticas
4. **Network isolation**: Use Private Endpoints quando possível

### Desenvolvimento
```sql
-- Template para criação de usuário com permissões limitadas
CREATE USER [app-user] WITH PASSWORD = 'StrongPassword123!';
ALTER ROLE db_datareader ADD MEMBER [app-user];
ALTER ROLE db_datawriter ADD MEMBER [app-user];
```

## 🔧 Troubleshooting

### Problemas Comuns

#### Erro de Conexão
```
Erro: "Cannot connect to server"
Soluções:
1. Verificar regras de firewall
2. Confirmar string de conexão
3. Testar conectividade de rede
4. Validar credenciais
```

#### Performance Lenta
```
Sintomas: Queries demoradas, timeouts
Diagnóstico:
1. Verificar DTU/vCore usage
2. Analisar Query Performance Insight  
3. Revisar planos de execução
4. Verificar bloqueios
```

#### Limite de Storage
```
Erro: "Database size limit reached"
Soluções:
1. Aumentar tier de serviço
2. Limpar dados desnecessários
3. Arquivar dados históricos
4. Implementar particionamento
```

### Comandos Úteis de Diagnóstico
```sql
-- Verificar uso de espaço
SELECT 
    DB_NAME() AS DatabaseName,
    CAST(SUM(size) * 8.0 / 1024 AS DECIMAL(10,2)) AS SizeMB
FROM sys.database_files;

-- Identificar queries demoradas
SELECT TOP 10 
    total_worker_time/execution_count AS avg_cpu_time,
    execution_count,
    SUBSTRING(st.text, (qs.statement_start_offset/2)+1,
    ((CASE qs.statement_end_offset
        WHEN -1 THEN DATALENGTH(st.text)
        ELSE qs.statement_end_offset
    END - qs.statement_start_offset)/2) + 1) AS statement_text
FROM sys.dm_exec_query_stats AS qs
CROSS APPLY sys.dm_exec_sql_text(qs.sql_handle) AS st
ORDER BY avg_cpu_time DESC;
```

## 📚 Recursos Adicionais

### Documentação Oficial
- [Azure SQL Database Documentation](https://docs.microsoft.com/azure/sql-database/)
- [Azure Database for MySQL](https://docs.microsoft.com/azure/mysql/)
- [Azure Database for PostgreSQL](https://docs.microsoft.com/azure/postgresql/)
- [Azure Cosmos DB](https://docs.microsoft.com/azure/cosmos-db/)

### Ferramentas Úteis
- **Azure Data Studio**: Cliente multiplataforma
- **SQL Server Management Studio**: Cliente Windows completo
- **Azure CLI**: Automação via linha de comando
- **Azure PowerShell**: Scripts de gerenciamento
- **Terraform**: Infrastructure as Code
- **ARM Templates**: Deployment templates

### Cursos e Certificações
- **AZ-900**: Azure Fundamentals
- **DP-900**: Azure Data Fundamentals  
- **AZ-104**: Azure Administrator
- **DP-300**: Azure Database Administrator

### Comunidade
- [Microsoft Q&A](https://docs.microsoft.com/answers/)
- [Stack Overflow - Azure](https://stackoverflow.com/questions/tagged/azure)
- [Reddit - r/AZURE](https://reddit.com/r/AZURE)
- [Azure Blog](https://azure.microsoft.com/blog/)

## 🤝 Contribuições

Este repositório é um material de estudo colaborativo. Contribuições são bem-vindas através de:

1. **Issues**: Reporte problemas ou sugestões
2. **Pull Requests**: Propose melhorias no conteúdo
3. **Discussões**: Compartilhe experiências e dicas
4. **Exemplos**: Adicione casos de uso reais

### Como Contribuir
1. Fork este repositório
2. Crie uma branch para sua feature (`git checkout -b feature/nova-secao`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova seção sobre X'`)
4. Push para a branch (`git push origin feature/nova-secao`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 📞 Suporte

Para questões específicas sobre este guia:
- Abra uma [issue](../../issues) no repositório
- Entre em contato através das [discussões](../../discussions)

Para suporte oficial do Azure:
- [Azure Support Plans](https://azure.microsoft.com/support/plans/)
- [Azure Documentation](https://docs.microsoft.com/azure/)

---

**⭐ Se este guia foi útil, considere dar uma estrela no repositório!**

*Última atualização: Maio 2024*