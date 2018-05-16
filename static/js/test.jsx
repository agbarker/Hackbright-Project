

class NameButton extends React.Component {
    
    constructor(props)  {
      super(props);
      this.state = {result: "?"};

      this.logName = this.logName.bind(this);
    }



    logName() {
        fetch('/name.json', {
        credentials: 'include'
        })
          .then((response) => response.json())
          .then((teacher) => { this.setState({result: "Your name is " + teacher.fname + " " + teacher.lname}) }
        // this.setState({result: name_result});

      )}
          
    
  

    render() {
        return (<button onClick={this.logName}>
                 <i> Get Name </i>
                 <b>{ this.state.result }</b>
               </button>
               );
    }
}




ReactDOM.render(
    <NameButton />,
    document.getElementById('test_this')
);


