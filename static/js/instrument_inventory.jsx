function NumberList(props) {
  const numbers = props.numbers;
  const listItems = numbers.map((number) =>
    <li key={number.toString()}>
      {number}
    </li>
  );
  return (
    <ul>{listItems}</ul>
  );
}



function logName() {
        fetch('/instrument-inventory.json', {
        credentials: 'include'
        })
          .then((response) => response.json())
          .then((instruments) => { this.setState({numbers: instruments) }
        // this.setState({result: name_result});

      )}




const numbers = [1, 2, 3, 4, 5];
ReactDOM.render(
  <NumberList numbers={numbers} />,
  document.getElementById('root')
);