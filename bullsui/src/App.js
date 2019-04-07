import React, { Component } from 'react';
import logo from './bullseye.png'
import ready from './ready-player-one-logo-png-2.png'
import explosion from './giphy.gif'
import './App.css';



class App extends Component {
  constructor (props) {
    super()
    this.imageRef = React.createRef();
    this.frameRef = React.createRef();
    this.x=this.y=1
    this.state = { visiableDot: true, redScreen: 0, fight: 0}
  } 
  

  newSocket = () => {
    var self = this
    self.exampleSocket = new WebSocket("ws://localhost:9999")
    console.log('new socket')
    self.exampleSocket.onmessage = function (event) {
      console.log('got event', event.data);
      let {offsetTop, offsetLeft} = JSON.parse(event.data)
      self.moveTarget({
        image: self.imageRef.current, 
        offsetTop, 
        offsetLeft
      })
    }
    self.exampleSocket.onclose = function (event) {
      console.log('disconnected', event);
      self.connected = false 
      setTimeout(function() { self.newSocket() }, 2000)
    }
    self.exampleSocket.onopen = function (event) {
      console.log('connected', event);
      if (event.type === 'open') {
        self.connected = true 
      }
    };

  }

  componentDidMount(_props) {
    var self = this
    self.exampleSocket = self.newSocket()
    /*
    let a = setInterval(function () {
      let offsetTop = self.y++;
      let offsetLeft = self.x++;
      self.moveTarget({image: self.imageRef.current, offsetTop, offsetLeft})
    }, 500)
    console.log(a)
    */
  }

  moveTarget = ({image, offsetTop, offsetLeft}) => {
    
    if (this.done) {
      return;
    }

    if (this.state.visiableDot == true) {
      this.setState({visiableDot: false})
      return
    }
	
    let img = image
    console.log('moveTarget')

    var frameW = this.frameRef.current.clientWidth - img.clientWidth
    var frameH = this.frameRef.current.clientHeight - img.clientHeight
    if (offsetTop <= 1) {
    	offsetTop *= frameH
    	offsetLeft *= frameW
	if (this.lastY && Math.abs(this.lastY - offsetTop) > 0.45) {
    console.log('DONE')
    var self=this
    this.setState({redScreen: 1});
    setTimeout(() => {
      self.setState({redScreen: 0});
    }, 250);
		this.lastY = null
		this.done = true
    setTimeout(() => {

      self.setState({fight: 1})
      setTimeout(function () {
        self.setState({fight: 0})

        self.done=false; console.log('READY AGAIN');
      }, 1000)
    }, 3000);
	}
    }
    else {
    	offsetTop %= frameH
    	offsetLeft %= frameW

    }
	this.lastY = offsetTop 

  img.width = '100%';
  img.opacity = 0;
  img.style.position = 'absolute';
  img.style.top = offsetTop + 'px';
  img.style.left = offsetLeft + 'px';
  img.style.display = "block";
  if (this.exampleSocket && this.connected) this.exampleSocket.send(JSON.stringify({offsetTop, offsetLeft}));
  }

  render() {
    return (
      
      
      <div ref={this.frameRef} className="corners" height="100%" width="100%">
     <div class="fight-container">
      <div class="fight" style={{opacity: this.state.fight}}> </div>
     </div>

      {/* <img src={ready} width="500" style={{position: 'absolute', top:0, bottom:0 ,left:0, right:0}} /> */}
      <div class="red-screen" style={{opacity: this.state.redScreen}}></div>

      {
         this.state.visiableDot ? <div class="circle_top_left"></div>:<div></div>
        
      }
      {
         this.state.visiableDot ? <div class="circle_bottom_right"></div>:<div></div>
      }
      
      { /* 
        <div class="top left"></div>
        <div class="top right"></div>
        <div class="bottom right"></div>
        <div class="bottom left"></div>
      */ }
       <img ref={this.imageRef} src={logo} className="App-logo" alt="logo"/>

 
         
        </div>
      
    );
  }
}

export default App;
