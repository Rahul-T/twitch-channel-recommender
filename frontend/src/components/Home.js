import React, { Component } from 'react'
import ReactLoading from "react-loading";
import "bootstrap/dist/css/bootstrap.css";
import { makeStyles } from '@material-ui/core/styles';
import GridList from '@material-ui/core/GridList';
import GridListTile from '@material-ui/core/GridListTile';

const classes = makeStyles(theme => ({
    root: {
      display: 'flex',
      flexWrap: 'wrap',
      justifyContent: 'space-around', 
      overflow: 'hidden',
      backgroundColor: theme.palette.background.paper,
    },
    gridList: {
      width: 500,
      height: 450,
    },
  }));

class Home extends Component {
    constructor(props) {
        super(props);
        this.state = {
            done: undefined,
            games: null
        };
    }

    componentDidMount() {
        setTimeout(() => {
          fetch("http://127.0.0.1:5000/games")
            .then(response => response.json())
            .then(obj => this.setState({  
                done: true,
                games: JSON.parse(JSON.stringify(obj))
            }));
        }, 1200);

      }

    render() {
        if(!this.state.done) {
            return <ReactLoading type={"bars"} color={"black"} />
        } else {
            
            // console.log(typeof JSON.parse(this.state.games))
            return (
                
                <div className={classes.root}>
                    <h3 style={{paddingTop : '20px', paddingBottom : '20px'}}>Which Game Do You Want To Watch?</h3>
                    <GridList cellHeight={75} className={classes.gridList} cols={5}>
                        <GridListTile>
                            <div>Any Game!</div>
                        </GridListTile>
                        {this.state.games.map(game => (
                        <GridListTile key={game}>
                            <div>{game}</div>
                        </GridListTile>
                        ))}
                    </GridList>
                </div>
            )
        } 
    }
}

export default Home