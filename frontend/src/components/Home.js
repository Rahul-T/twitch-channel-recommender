import React, { Component } from 'react'
import ReactLoading from "react-loading";
import "bootstrap/dist/css/bootstrap.css";
import { makeStyles } from '@material-ui/core/styles';
import GridList from '@material-ui/core/GridList';
import GridListTile from '@material-ui/core/GridListTile';
import ToggleButton from '@material-ui/lab/ToggleButton';
import ToggleButtonGroup from '@material-ui/lab/ToggleButtonGroup';
import Button from '@material-ui/core/Button';

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
            recommendation: null
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
        console.log("Form submitted")
        console.log(this.state.selectedGame)
        console.log(this.state.selectedEmotion)
        this.setState({gettingRecommendation: true})
        setTimeout(() => {
            fetch(`http://127.0.0.1:5000/recommendation?emotion=${this.state.selectedEmotion}&game=${this.state.selectedGame}`)
              .then(response => response.json())
              .then(obj => this.setState({  
                  gettingRecommendation: false,
                  recommendation: JSON.parse(JSON.stringify(obj))
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
                        <h4 style={{position: 'absolute', left: '50%', top: '40%',transform: 'translate(-50%, -50%)'}}>
                            We recommend <span style={{color: '#6441a5'}}>{this.state.recommendation}</span>! &nbsp;
                            Channel link: <a href={url} target="_blank" rel="noopener noreferrer">{url}</a>
                        </h4>
                        <Button variant="outlined" onClick={this.refreshPage}
                        style={{
                            position: 'absolute',
                            left: '50%',
                            top: '50%',
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
                            Any Game!
                        </ToggleButton>
                        </GridListTile>
                        {this.state.games.map(game => (
                        <GridListTile key={game}>
                            <ToggleButton size="small" value={game} selected={this.state.selectedGame === game} onClick={() => this.gameSelected(game)}>
                                {game}
                            </ToggleButton>
                        </GridListTile>
                        ))}
                    </GridList>
                    
                    <h4 style={{paddingTop : '20px', paddingBottom : '20px'}}>Select Desired Mood Of Stream</h4>

                    <ToggleButtonGroup aria-label="Basic example" exclusive>
                        <ToggleButton variant="text" value="Anger" selected={this.state.selectedEmotion === "Anger"} onClick={() => this.emotionSelected("Anger")}>Anger</ToggleButton>
                        <ToggleButton variant="text" value="Disgust" selected={this.state.selectedEmotion === "Disgust"} onClick={() => this.emotionSelected("Disgust")}>Disgust</ToggleButton>
                        <ToggleButton variant="text" value="Fear" selected={this.state.selectedEmotion === "Fear"} onClick={() => this.emotionSelected("Fear")}>Fear</ToggleButton>
                        <ToggleButton variant="text" value="Joy" selected={this.state.selectedEmotion === "Joy"} onClick={() => this.emotionSelected("Joy")}>Joy</ToggleButton>
                        <ToggleButton variant="text" value="Sadness" selected={this.state.selectedEmotion === "Sadness"} onClick={() => this.emotionSelected("Sadness")}>Sadness</ToggleButton>
                        <ToggleButton variant="text" value="Surprise" selected={this.state.selectedEmotion === "Surprise"} onClick={() => this.emotionSelected("Surprise")}>Surprise</ToggleButton>
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