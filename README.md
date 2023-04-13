Payment Processor
==============
Durante uma reunião, você decidiu que é necessário melhorar o processo de pagamentos na empresa. Ao chegar em casa, você se depara com uma longa lista de regras a serem implementadas, incluindo a criação de guias de remessa para produtos físicos, guias de remessa duplicadas para livros, ativação de novas associações, upgrades em associações existentes e envio de e-mails de notificação, entre outras tarefas. A implementação dessas regras pode parecer complicada e arbitrária, e você sabe que novos casos especiais surgirão assim que o sistema estiver em operação. Para lidar com essa complexidade e a necessidade de mudanças futuras, é essencial que o software seja flexível e escalável.

Uma abordagem adequada seria a aplicação do design pattern Strategy, passando a responsabilidade da criação dos objetos com o _Factory Method_, com isso deixamos o software flexível. Mas como estamos lidando com um cenário de pagamentos, é crucial garantir um tempo de inatividade o mais próximo possível de zero. Embora seja tentador trabalhar com um aplicativo monolítico por sua facilidade de uso, cada nova regra exigiria um novo deploy, o que seria um grande problema para a equipe de desenvolvimento. Isso porque não seria possível segmentar a equipe em unidades de negócio específicas, o que aumentaria a carga cognitiva dos profissionais para entender as regras de negócio. Como resultado, o tempo para corrigir eventuais bugs e entregar novas funcionalidades seria significativamente maior. É evidente que um aplicativo monolítico seria muito custoso para acomodar todos os tipos e regras de pagamentos.

O aplicativo monolítico seria custoso para acomodar todas as regras de pagamentos. Por outro lado, a arquitetura de _microservices_ é complexa e exige a automatização da infraestrutura, monitoramento, logs, trace, service registry, service discovery e outras etapas importantes, além de garantir a consistência de dados, o que pode ser difícil. O fluxo síncrono vs. assíncrono também é um fator a ser considerado, uma vez que a consistência eventual pode afetar a interação com o usuário final.

Por isso, a melhor escolha é a criação de um aplicativo central que conheça apenas os recursos de alto nível, permitindo a aplicação de plug-ins para lidar com as regras de complexidade de cada pagamento. Cada plug-in pode ser uma pequena unidade para lidar com as regras específicas de cada tipo de pagamento. Essa abordagem permite enviar um aplicativo simples para um ou mais inversores específicos que temos, usando a mesma infraestrutura.

Foi decidido criar um sistema com a possibilidade de extensão por meio de plugins. Para adicionar um novo tipo de pagamento, basta criar uma nova classe de serviço de pagamento que implemente a interface *PaymentPluginInterface* e adicioná-la ao dicionário *services_by_type* na classe *PaymentFactory*. Os plugins podem ser organizados em arquivos separados na pasta plugins, e cada plugin tem seu próprio ciclo de vida independente, podendo conter funcionalidades adicionais e códigos personalizados para estender as funcionalidades básicas do sistema. É importante manter o mínimo de comunicação entre os plugins para evitar possíveis problemas de dependência.

Caso a arquitetura baseada em plugins não seja suficiente para lidar com o sistema ou se deseje escalar os plugins de forma independente, é possível evoluir a aplicação para outra arquitetura, como a de _microservices_ usando o padrão de arquitetura em camadas ou implementar os componentes event processors. Essas arquiteturas permitem a escalabilidade independente de cada componente e uma maior flexibilidade na gestão da aplicação.

<h1 align="center">
    <img src="https://i.imgur.com/A5mDiEI.png">
</h1>


### Código 
O código contém basicamente 2 partes importante, a factory de plugin e o load do plugin iremos começar pela mais importante que é a classe *PaymentServiceFactory* que contém métodos estáticos que permitem o registro de novos tipos de pagamento e sua criação posterior. O método *_by_type_* retorna o tipo de pagamento registrado, enquanto o método register registra um novo tipo de pagamento. O método unregister remove um tipo de pagamento previamente registrado.

O método create cria um novo pagamento do tipo especificado em um objeto JSON passado como argumento. Este método realiza uma cópia dos argumentos, extrai o tipo de pagamento do objeto JSON e tenta recuperar a função de criação correspondente a partir do registro de um tipo de pagamento. Se a função de criação for encontrada, ela é invocada e o pagamento é retornado como um objeto do tipo *PaymentPluginInterface*. Caso contrário, uma exceção *PaymentException* é lançada indicando que o tipo de pagamento é desconhecido.

Este código é uma boa solução para casos em que a aplicação de pagamentos precisa ser flexível e extensível, permitindo a adição de novos tipos de pagamento sem a necessidade de modificar o código existente. A documentação do código é clara e detalhada, tornando fácil o entendimento de como a _Factory_ funciona e como utilizá-la na aplicação.

Este código é um carregador de plugins simples que permite que os desenvolvedores adicionem novos recursos a um sistema sem precisar modificar o código existente. Ele importa módulos a partir do diretório "plugins" especificado e chama o método *register* em cada um desses módulos. O objetivo principal da classe "ModuleInterface" é servir como uma interface de plugin, garantindo que cada plugin tenha um método *register* que possa ser chamado pelo carregador de plugins.

A função *import_module* é usada para importar um módulo de um nome de arquivo especificado e a função *load_plugins* é usada para carregar uma lista de módulos de plugins especificados e chamar o método *register* em cada um desses módulos. Se um módulo não tiver um método *register*, ele será ignorado. O diretório de plugins padrão é especificado na constante *PLUGIN_FOLDER*.


### Adicionar um novo plugin
Essa parte visa desmistificar como podemos adicionar um novo plugin no sistema 

*Passo 1*: Criar o Plugin de Pagamento
Crie um novo arquivo Python para o _Payment Plugin_ e implemente o _PaymentPluginInterface_. Essa interface define os métodos que devem ser implementados pelo Plugin de Pagamento. Por exemplo:

```python

from payment_app.payment_app.core.paymentPluginInterface import PaymentPluginInterface

class BoletoPaymentPlugin(PaymentPluginInterface):
    def __init__(self, arguments):
        # initialize the plugin with arguments from JSON data
        pass

    def process_payment(self):
        # process the payment
        pass

def register() -> None:
    PaymentServiceFactory.register(PaymentType.Boleto.value, BoletoPaymentPlugin)

```

*Passo 2*: Adicionar ao Json
Crie um objeto de dados JSON com o tipo definido para o novo tipo de plug-in de pagamento e quaisquer argumentos necessários.
Por exemplo:
```json

{
  "plugins": ["plugins.boletoPaymentPlugin"],
  "characters": [
    {
      "type": "Boleto",
      "name": "BoletoPaymentPlugin"
    }
  ]
}

```

Como usar
----------

O script `main.py` contém um exemplo de utilização do processador de pagamento. Você pode executá-lo com o comando:

`python main.py`


Trabalhos futuros
------------
Olhando para o futuro, uma das principais vantagens do uso de _microservices_ em um cenário de pagamentos é a alta disponibilidade que pode ser alcançada com a utilização de vários serviços independentes que trabalham em conjunto. Cada serviço pode ser implementado, testado e implantado separadamente, permitindo atualizações sem que seja necessário interromper a aplicação inteira. Além disso, cada serviço pode ser desenvolvido por um time específico, possibilitando a segmentação do time de desenvolvimento em unidades de negócio específicas. Isso facilita a compreensão das regras de negócio e, consequentemente, reduz o tempo para correção de erros e entrega de novas funcionalidades.

É importante lembrar que a implementação de _microservices_ pode exigir a criação de um ambiente de desenvolvimento, homologação e deploy automatizado, o que pode elevar o custo e a complexidade da aplicação. No entanto, em cenários em que é crucial ter uma alta disponibilidade e escalabilidade, essa arquitetura é uma excelente opção. Entretanto, é importante ressaltar que a escolha por esse tipo de arquitetura deve ser feita com base nas necessidades e objetivos específicos do negócio.

No presente momento, com base no documento apresentado, não parece ser necessário implementar _microservices_. Entretanto, é importante ter em mente que a evolução do negócio e a expansão do sistema podem exigir essa mudança. Caso isso ocorra, poderíamos usar o system design apresentado abaixo como ponto de partida para a implementação dos _microservices_.

<h1 align="center">
    <img src="https://i.imgur.com/QvaU8Lv.jpg">
</h1>


Contribuição
------------

Contribuições são bem-vindas! Se você quiser contribuir com este projeto, siga as etapas abaixo:

1.  Faça um fork deste repositório
2.  Crie uma branch para sua feature (`git checkout -b feature/sua-feature`)
3.  Faça o commit das mudanças (`git commit -am 'Adiciona sua feature'`)
4.  Faça o push para o branch (`git push origin feature/sua-feature`)
5.  Abra um pull request neste repositório

Licença
-------

Este projeto está licenciado sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.
