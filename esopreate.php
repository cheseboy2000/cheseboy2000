<?php
require '../vendor/autoload.php';

use Elasticsearch\ClientBuilder;
Use Faker\Factory;
class EsHandle{
	private $EsClient = null;
	private $faker = null;
    /**
     * 为了简化测试，本测试默认只操作一个Index，一个Type，
     * 所以这里固定为 megacorp和employee
     */
    private $index = 'megacorp';
    private $type = 'employee';
	function __construct(){
		$EsClient=ClientBuilder::create()->setHosts(['http://elastic:zhulong@123@es-cn-v0h1cmy900004dfhs.elasticsearch.aliyuncs.com:9200'])->build();
		$this->EsClient=$EsClient;
		$this->faker = Faker\Factory::create('zh_CN');
	}
	 /**
     * 批量生成文档
     * @param $num
     */
    public function generateDoc($num = 100) {
        foreach (range(1,$num) as $item) {
            $this->putDoc([
                'first_name' => $this->faker->name,
                'last_name' => $this->faker->name,
                'age' => $this->faker->numberBetween(20,80)
            ]);
        }
    }
    /**
     * 删除一个文档
     * @param $id
     * @return array
     */
    public function delDoc($id) {
        $params = [
            'index' => $this->index,
            'type' => $this->type,
            'id' =>$id
        ];
        return $this->EsClient->delete($params);
    }
    /**
     * 搜索文档，query是查询条件
     * @param array $query
     * @param int $from
     * @param int $size
     * @return array
     */
    public function search($query = [], $from = 0, $size = 5) {
//        $query = [
//            'query' => [
//                'bool' => [
//                    'must' => [
//                        'match' => [
//                            'first_name' => 'Cronin',
//                        ]
//                    ],
//                    'filter' => [
//                        'range' => [
//                            'age' => ['gt' => 76]
//                        ]
//                    ]
//                ]
//
//            ]
//        ];
        $params = [
            'index' => $this->index,
//            'index' => 'm*', #index 和 type 是可以模糊匹配的，甚至这两个参数都是可选的
            'type' => $this->type,
            //'_source' => ['first_name','age'], // 请求指定的字段
            'body' => array_merge([
                'from' => $from,
                'size' => $size
            ],$query)
        ];
        return $this->EsClient->search($params);
    }

    /**
     * 一次获取多个文档
     * @param $ids
     * @return array
     */
    public function getDocs($ids) {
        $params = [
            'index' => $this->index,
            'type' => $this->type,
            'body' => ['ids' => $ids]
        ];
        return $this->EsClient->mget($params);
    }

    /**
     * 获取单个文档
     * @param $id
     * @return array
     */
    public function getDoc($id) {
        $params = [
            'index' => $this->index,
            'type' => $this->type,
            'id' =>$id
        ];
        return $this->EsClient->get($params);
    }

    /**
     * 更新一个文档
     * @param $id
     * @return array
     */
    public function updateDoc($id) {
        $params = [
            'index' => $this->index,
            'type' => $this->type,
            'id' =>$id,
            'body' => [
                'doc' => [
                    'first_name' => '张',
                    'last_name' => '三',
                    'age' => 99
                ]
            ]
        ];
        return $this->EsClient->update($params);
    }

    /**
     * 添加一个文档到 Index 的Type中
     * @param array $body
     * @return void
     */
    public function putDoc($body = []) {
        $params = [
            'index' => $this->index,
            'type' => $this->type,
//            'id' => 1, #可以手动指定id，也可以不指定随机生成
            'body' => $body
        ];
        $this->EsClient->index($params);
    }
    /**
     * 删除所有的 Index
     */
    public function delAllIndex() {
        $indexList = $this->esStatus()['indices'];
        foreach ($indexList as $item => $index) {
            $this->delIndex();
        }
    }
    /**
     * 获取 ES 的状态信息，包括index 列表
     * @return array
     */
    public function esStatus() {
        return $this->EsClient->indices()->stats();
    }

    /**
     * 创建一个索引 Index （非关系型数据库里面那个索引，而是关系型数据里面的数据库的意思）
     * @return void
     */
    public function createIndex() {
        $this->delIndex();
        $params = [
            'index' => $this->index,
            'body' => [
                'settings' => [
                    'number_of_shards' => 2,
                    'number_of_replicas' => 0
                ]
            ]
        ];
        $this->EsClient->indices()->create($params);
    }

    /**
     * 检查Index 是否存在
     * @return bool
     */
    public function checkIndexExists() {
        $params = [
            'index' => $this->index
        ];
        return $this->EsClient->indices()->exists($params);
    }

    /**
     * 删除一个Index
     * @return void
     */
    public function delIndex() {
        $params = [
            'index' => $this->index
        ];
        if ($this->checkIndexExists()) {
            $this->EsClient->indices()->delete($params);
        }
    }

    /**
     * 获取Index的文档模板信息
     * @return array
     */
    public function getMapping() {
        $params = [
            'index' => $this->index
        ];
        return $this->EsClient->indices()->getMapping($params);
    }

    /**
     * 创建文档模板
     * @return void
     */
    public function createMapping() {
        $this->createIndex();
        $params = [
            'index' => $this->index,
            'type' => $this->type,
            'body' => [
                $this->type => [
                    '_source' => [
                        'enabled' => true
                    ],
                    'properties' => [
                        'id' => [
                            'type' => 'integer'
                        ],
                        'first_name' => [
                            'type' => 'text',
                            'analyzer' => 'ik_max_word'
                        ],
                        'last_name' => [
                            'type' => 'text',
                            'analyzer' => 'ik_max_word'
                        ],
                        'age' => [
                            'type' => 'integer'
                        ]
                    ]
                ]
            ]
        ];
        $this->EsClient->indices()->putMapping($params);
        $this->generateDoc();
    } 
}
$api= new EsHandle();
$query=[
	'query' => [
		'bool'=>[
			'must'=>[
				'match' => [
	            	'first_name' =>[
	            		'query'=>'乔旭',
	            		//"operator"=> "and",
	            	]
	        	]
	        ]
		]
    ]
];
$res=$api->search($query);
print_r($res);
?>
