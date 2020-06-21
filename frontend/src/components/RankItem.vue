<template>
  <div>
    <div class="small"><span>空 100倍</span><span>火币</span><span>14天25小时</span></div>
    <b-media>
      <template v-slot:aside>
        <b-img blank blank-color="#ccc" width="64" alt="placeholder"></b-img>
      </template>
      <h5 class="mt-0">追梦人物</h5>
      <p>
        Cras sit amet nibh libero, in gravida nulla. Nulla vel metus scelerisque ante sollicitudin.
      </p>
    </b-media>
    <div class="d-flex justify-content-between">
      <span><span>2794USDT</span><br><span>本金</span></span>
      <span><span>1899USDT</span><br><span>余额</span></span>
      <span><span>19.3%</span><br><span>收益率</span></span>
      <span><span>145USDT</span><br><span>收益额</span></span>
    </div>
  </div>
</template>

<script>
    export default {
        name: 'HelloWorld',
        props: {
            msg: String
        }
    }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  h3 {
    margin: 40px 0 0;
  }

  ul {
    list-style-type: none;
    padding: 0;
  }

  li {
    display: inline-block;
    margin: 0 10px;
  }

  a {
    color: #42b983;
  }
</style>
