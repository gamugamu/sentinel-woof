
Vue.component('step', {
  props: ['title', 'method', 'url_root', 'route', 'required_bearer', 'use', 'curl_cmd',
  'data', 'm_return', 'require_oauth', 'require_login', 'return_id', 'json_return', 'dyn_value'],
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
             <th><i></i></th>
         </tr>
       </thead>
       <tbody>
       <tr v-for="(v, k) in data">
          <th>{{k}}</th>
          <td>{{v}}</td>
          <td v-if="dyn_value !== undefined && k in dyn_value" >
            <div class="input-field dyno_value">
              <input v-model="dyn_value[k]" id="first_name2" type="text" class="validate">
              <label for="first_name2">{{k}}</label>
            </div>
          </td>
       </tr>
       </tbody>
       </table>

       <table class="bordered" v-if="this.dyn_value != undefined">
          <tbody>
            <tr v-for="(v, k) in data">

            </tr>
          </tbody>
        </table>

      <pre><code class="language-bash line-numbers">{{curl_command}}</code></pre>
      <div>
        <h5>Return</h5>
          <div v-show="loading" class="progress">
            <div class="indeterminate"></div>
          </div>
          <div class="return">
            <pre>
              {{m_json_return}}
            </pre>
            <template v-if="require_oauth">
              <a  v-on:click="call_curl_cmd()"
                  class="test cyan darken-1 waves-effect waves-light btn right top"
                  v-bind:class="{ disabled: !can_test_oauth}" ><i class="material-icons right">confirmation_number</i>Test</a>
            </template>
            <template v-if="require_login">
              <a  v-on:click="call_curl_cmd()"
                  class="test orange darken-3 waves-effect waves-light btn right top"
                  v-bind:class="{ disabled: !can_test_login}"><i class="material-icons right">verified_user</i>test</a>
            </template>
          </div>
      </div>
    </div>
  `,computed: {
    // un accesseur (getter) calculé
    curl_command: {
      get: function () {
      // `this` pointe sur l'instance vm
      var cmd = "curl -i -H \"Content-Type: application/json\" "
      if (this.required_bearer == "true"){
          cmd += '-i -H "Authorization: Bearer ' + this.$parent.session_token + '" '
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
      }else if(this.method != "GET"){
        cmd += "-X " + this.method + " "
      }

      this.m_json_return = "\n" + this.pretty_json(this.m_return)
      cmd += this.url_root + this.route;

      return cmd
      }
    },
    can_test_oauth:{
        get: function () {
          return  this.$parent.client_id.length != 0 &&
                  this.$parent.provider.length  != 0 &&
                  this.$parent.auth_login.length != 0
        }
    },
    can_test_login:{
        get: function () {
          return  this.$parent.session_token.length != 0
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
      return obj
    },
    call_curl_cmd(cmd){
      _this         = this
      _this.loading = true

      axios.post('/test/curl_cmd', {
        command: this.curl_command
      })
      .then(function (response) {
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
    client_id:  sessionStorage.getItem("client_id")   ? sessionStorage.getItem("client_id")   : "",
    provider:   sessionStorage.getItem("provider")    ? sessionStorage.getItem("provider")    : "",
    auth_login: sessionStorage.getItem("auth_login")  ? sessionStorage.getItem("auth_login")  : "",
    session_token: sessionStorage.getItem("session_token")  ? sessionStorage.getItem("session_token")  : "",
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
        },
        'session_token': function(val, oldVal){
          sessionStorage.setItem("session_token", val)
        }
    }
});
