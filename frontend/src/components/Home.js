import React, { Component } from 'react'
import { Text } from 'react-native';
import ReactLoading from "react-loading";
import "bootstrap/dist/css/bootstrap.css";
import { makeStyles } from '@material-ui/core/styles';
import GridList from '@material-ui/core/GridList';
import GridListTile from '@material-ui/core/GridListTile';
import ToggleButton from '@material-ui/lab/ToggleButton';
import ToggleButtonGroup from '@material-ui/lab/ToggleButtonGroup';
import Button from '@material-ui/core/Button';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import Paper from '@material-ui/core/Paper';

const classes = makeStyles(theme => ({
    root: {
      display: 'flex',
      flexWrap: 'wrap',
      justifyContent: 'space-around' , 
      overflow: 'hidden',
      backgroundColor: theme.palette.background.paper
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
            startup: false,
            games: null,
            selectedGame: "Any Game!",
            selectedEmotion: "Joy",
            gettingRecommendation: false,
            recommendation: null,
            emotions: null
        };
    }

    componentDidMount() {
        setTimeout(() => {
          fetch("http://127.0.0.1:5000/games")
            .then(response => response.json())
            .then(obj => this.setState({  
                startup: true,
                games: JSON.parse(JSON.stringify(obj))
            }));
        }, 1200);

      }


    gameSelected = (game) => {
        this.setState({ selectedGame: game })
    }

    emotionSelected = (emotion) => {
        this.setState({ selectedEmotion: emotion })
    }

    getRecommendation = (e) => {
        e.preventDefault()
        this.setState({gettingRecommendation: true})
        setTimeout(() => {
            fetch(`http://127.0.0.1:5000/recommendation?emotion=${this.state.selectedEmotion}&game=${this.state.selectedGame}`)
              .then(response => response.json())
              .then(obj => this.setState({  
                  gettingRecommendation: false,
                  recommendation: JSON.parse(JSON.stringify(obj))['stream'],
                  emotions:  JSON.parse(JSON.stringify(obj))['emotions']
              }));
          }, 1200);
    }
    
    refreshPage() {
        window.location.reload(false);
    }

    render() {
        if(!this.state.startup) {
            return <div>
                        <h4 style={{display: 'flex',  justifyContent:'center', alignItems:'center', height: '90vh'}}>
                            Starting up
                            <ReactLoading type={"bars"} color={"black"} /><br />
                        </h4>
                    </div>
        } else if(this.state.gettingRecommendation) {
            return  <div>
                        <h4 style={{display: 'flex',  justifyContent:'center', alignItems:'center', height: '90vh'}}>
                            Getting recommendation (may take several minutes)
                            <ReactLoading type={"bars"} color={"black"} />
                        </h4>
                    </div>
        } else if(this.state.recommendation) {
            const url = `https://www.twitch.tv/${this.state.recommendation}`
            return  <div>
                        <h4 style={{position: 'absolute', left: '50%', top: '25%',transform: 'translate(-50%, -50%)'}}>
                            We recommend <span style={{color: '#6441a5'}}>{this.state.recommendation}</span>!
                            <br/>Channel link: <a href={url} target="_blank" rel="noopener noreferrer">{url}</a>
                        </h4>
                        <h6 style={{position: 'absolute', left: '50%', top: '51%',transform: 'translate(-50%, -50%)'}}>
                     
                            <Paper className={classes.root}>
                                <Table className={classes.table} size="small" aria-label="a dense table">
                                    <caption>Number of messages for each respective emotion</caption>
                                    <TableHead>
                                    <TableRow>
                                        <TableCell align="center">Emotion</TableCell>
                                        <TableCell align="center">Messages</TableCell>
                                    </TableRow>
                                    </TableHead>
                                    <TableBody>
                                    
                                    {Object.keys(this.state.emotions).map((key, index) => ( 
                                        this.state.selectedEmotion === key ? 
                                            <TableRow key={key}>
                                                <TableCell key={index} align="center">
                                                    <Text style={{fontWeight: 'bold', backgroundColor: 'yellow'}}>{key}</Text>
                                                </TableCell>
                                                <TableCell key={index} align="center">
                                                    <Text style={{fontWeight: 'bold', backgroundColor: 'yellow'}}>{this.state.emotions[key]}</Text>
                                                </TableCell>
                                            </TableRow> : 
                                            <TableRow key={key}>
                                                <TableCell key={index} align="center">{key}</TableCell>
                                                <TableCell key={index} align="center">{this.state.emotions[key]}</TableCell>
                                            </TableRow>
                                    ))}
                                    
                                    </TableBody>
                                </Table>
                                </Paper>
                        </h6>
                        <Button variant="outlined" onClick={this.refreshPage}
                        style={{
                            position: 'absolute',
                            left: '50%',
                            top: '75%',
                            transform: 'translate(-50%, -50%)'
                            }}>
                                Get New Recommendation!</Button>
                    </div>
        } else {            
            return (
                <div className={classes.root}>
                    <h4 style={{paddingTop : '20px', paddingBottom : '20px'}}>Which Game Do You Want To Watch?</h4>

                    <GridList cellHeight={65} className={classes.gridList} cols={5}>
                        <GridListTile>
                        <ToggleButton size="small" value="Any Game!" selected={this.state.selectedGame === "Any Game!"} onClick={() => this.gameSelected("Any Game!")}>
                            <Text style={{color: 'black'}}>Any Game!</Text>
                        </ToggleButton>
                        </GridListTile>
                        {this.state.games.map(game => (
                        <GridListTile key={game}>
                            <ToggleButton size="small" value={game} selected={this.state.selectedGame === game} onClick={() => this.gameSelected(game)}>
                                <Text style={{color: 'black'}}>{game}</Text>
                            </ToggleButton>
                        </GridListTile>
                        ))}
                    </GridList>
                    
                    <h4 style={{paddingTop : '20px', paddingBottom : '20px'}}>Select Desired Mood Of Stream</h4>

                    <ToggleButtonGroup aria-label="Basic example" exclusive>
                        <ToggleButton variant="text" value="Anger" selected={this.state.selectedEmotion === "Anger"} onClick={() => this.emotionSelected("Anger")}>
                            <Text style={{fontWeight: 'bold', color: 'red'}}>Anger</Text>
                        </ToggleButton>
                        <ToggleButton variant="text" value="Disgust" selected={this.state.selectedEmotion === "Disgust"} onClick={() => this.emotionSelected("Disgust")}>
                            <Text style={{fontWeight: 'bold', color: 'green'}}>Disgust</Text>
                        </ToggleButton>
                        <ToggleButton variant="text" value="Fear" selected={this.state.selectedEmotion === "Fear"} onClick={() => this.emotionSelected("Fear")}>
                            <Text style={{fontWeight: 'bold', color: 'orange'}}>Fear</Text>
                        </ToggleButton>
                        <ToggleButton variant="text" value="Joy" selected={this.state.selectedEmotion === "Joy"} onClick={() => this.emotionSelected("Joy")}>
                            <Text style={{fontWeight: 'bold', color: '#dbdb00'}}>Joy</Text>
                        </ToggleButton>
                        <ToggleButton variant="text" value="Sadness" selected={this.state.selectedEmotion === "Sadness"} onClick={() => this.emotionSelected("Sadness")}>
                            <Text style={{fontWeight: 'bold', color: 'blue'}}>Sadness</Text>
                        </ToggleButton>
                        <ToggleButton variant="text" value="Surprise" selected={this.state.selectedEmotion === "Surprise"} onClick={() => this.emotionSelected("Surprise")}>
                            <Text style={{fontWeight: 'bold', color: 'purple'}}>Surprise</Text>
                        </ToggleButton>
                    </ToggleButtonGroup>

                    <form style={{paddingTop : '20px'}} onSubmit={this.getRecommendation}>
                        <Button variant="outlined" type="submit">Get Recommendation!</Button>
                    </form>
                </div>
            )
        } 
    }
}

export default Home