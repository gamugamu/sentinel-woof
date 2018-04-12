
Vue.component('step', {
  props: ['title', 'method', 'url_root', 'route', 'required_bearer', 'use', 'curl_cmd', 'data', 'm_return', 'return_id', 'json_return'],
  template: `
    <div>
      <h5 v-if="title">• {{title}}</h5>
      <h5 v-else></br></h5>
      <b class="orange darken-3 white-text method">{{method}}</b> {{url_root}}<b class="cyan lighten-5">{{route}}</b></route>
      <p><i>{{use}}</i></p>
      <table class="bordered" v-if="this.data != undefined">
       <thead>
         <tr>
             <th><i>key</i></th>
             <th><i>value</i></th>
         </tr>
       </thead>
       <tbody>
       <tr v-for="(v, k) in data">
          <th>{{k}}</th>
          <td>{{v}}</td>
       </tr>
       </tbody>
       </table>
      <pre><code class="language-bash line-numbers">{{curl_command}}</code></pre>
      <div>
        <h5>Return</h5>
          <div v-show="loading" class="progress">
            <div class="indeterminate"></div>
          </div>
          <pre class="return margin_tight">
            {{m_json_return}}
            <a  v-on:click="call_curl_cmd()" class="test orange darken-3 waves-effect waves-light btn right top">Teste</a>
          </pre>
      </div>
    </div>
  `,computed: {
    // un accesseur (getter) calculé
    curl_command: {
      get: function () {
      // `this` pointe sur l'instance vm
      var cmd = "curl -i -H \"Content-Type: application/json\" "
      if (this.required_bearer == "true"){
          cmd += '-i -H "Authorization: Bearer XXXX_TOKEN_XXXX" '
      }

      if (this.curl_cmd != undefined){
        cmd += "-X " + this.method + " -d '{"

        for(var key in this.curl_cmd){
          var value = this.curl_cmd[key]

          if ( value.charAt(0) == '*' ) {
            k = value.substr(1, value.lenght);
            v = typeof this.$parent._data[k] !== 'undefined' ? this.$parent._data[k] : ""

            cmd += "\"" + key + "\":" + "\"" + v +  "\", "
          }else{
            cmd += "\"" + key + "\":" + "\"" + value +  "\", "
          }
        }
        cmd = cmd.slice(0, -2); // ', '
        cmd += "}' "
      }

      console.log("--> ", this, this.pretty_json(this.m_return));
      this.m_json_return = "\n" + this.pretty_json(this.m_return)
      cmd += this.url_root + this.route;

      return cmd
      }
    }
  },
  data: function () {
      return {
          m_json_return: this.json_return,
          loading: false
      };
  },
  methods: {
    pretty_json(format){
      var obj = JSON.parse(format);
      obj     = JSON.stringify(obj, undefined, 2);
      console.log("p_t", obj);
      return obj
    },
    call_curl_cmd(cmd){

      _this         = this
      _this.loading = true

      axios.post('/test/curl_cmd', {
        command: this.curl_command
      })
      .then(function (response) {
        console.log(response.data);
        _this.m_json_return = "\n" + response.data
        _this.loading = false
      })
      .catch(function (error) {
        console.log(error);
        _this.m_json_return = error
        _this.loading = false
      });
    }
  }
})

var app = new Vue({
  el: '#app',
  delimiters: ['${', '}'],
  data:{
    client_id: sessionStorage.getItem("client_id"),
    provider: sessionStorage.getItem("provider"),
    auth_login: sessionStorage.getItem("auth_login"),
  },
  watch: {
        'client_id': function(val, oldVal){
          sessionStorage.setItem("client_id", val)
        },
        'provider': function(val, oldVal){
          sessionStorage.setItem("provider", val)
        },
        'auth_login': function(val, oldVal){
          sessionStorage.setItem("auth_login", val)
        }
    }
});
