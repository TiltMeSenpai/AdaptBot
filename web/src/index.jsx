import React, {Component} from 'react'
import ReactDOM, {render} from 'react-dom'
import ReactDomServer from 'react-dom/server'
import {Router, Route, Link, browserHistory} from 'react-router'
import Api from './api.jsx'

class App extends Component {
  constructor(props){
    super(props)
    this.state = {}
  }
  render() {
    return (
      <div>
        <nav>
          <div className="nav-wrapper">
            <Link to="/" className="brand-logo">AdaptBot</Link>
            <ul id="nav-mobile" className="right hide-on-med-and-down">
              <li><Link to='/keys'>API Keys</Link></li>
              <li><Link to='/skills'>Skills</Link></li>
              <li><Link to='/logs'>Logs</Link></li>
              <User user={this.state.user}/>
            </ul>
          </div>
        </nav>
        {this.props.children}
      </div>
    )
  }

  componentDidMount(){
    window.callbacks.setState = this.setState.bind(this)
  }

  componentWillUpdate(nextProps, nextState){
    var api = new Api()
    console.log(nextState)
    api.setSession(nextState.session)
    api.setSecret(nextState.hmac_key)
    if(this.state.session != nextState.session){
      // If session changes, login or logout probably occured
      api.request('POST', '/user').then((value)=>{window.callbacks.setState({'user':value})})
    }
  }
}

class User extends Component {
  render() {
      if (typeof this.props.user != 'undefined') {
        return (
          <li>
            <a href='#' data-activates="user-panel" className="dropdown-button btn">
              {this.props.user.username}
            </a>
            <ul className="dropdown-content" id="user-panel">
              <li>
                <span>{this.props.user.username}#{this.props.user.discriminator}</span>
              </li>
            </ul>
          </li>
          )
      }else {
        return (
          <li>
            <div className="waves-effect waves-light btn" onClick={this.doLogin}>
              Login<span className="tiny material-icons">open_in_new</span>
            </div>
          </li>
        )
      }
  }

  componentDidMount(){
    var loginCallback = function(m){
      if(m.isTrusted){
        window.callbacks.setState(m.data)
      }
      window.removeEventListener("message", loginCallback)
    }
    if(this.props.user === undefined){
      console.log("Not logged in, adding listeners")
      window.addEventListener('message', loginCallback)
    }
  }

  componentDidUpdate(){
    if(this.props.user !== undefined){
      console.log("Logged in as "+this.props.user.username)
      $(".dropdown-button").dropdown({constrain_width: false})
    }
  }

  doLogin(){
      var popout = window.open("/login", "Login")
    }
}

class KeyList extends Component {
  render() {
    return <div>Not yet</div>
  }
}

class SkillList extends Component {
  render() {
    return <div>Not yet</div>
  }
}

class Skill extends Component {
  render() {
    return <div>Not yet</div>
  }
}
render((
    <Router history={browserHistory}>
        <Route path="/" component={App}>
            <Route path="keys" component={KeyList}/>
            <Route path="skills" component={SkillList}>
                <Route path="/skills/:skillId" component={Skill}/>
            </Route>
        </Route>
    </Router>
), document.getElementById('app'))
