import React, { Component } from 'react';

class Item extends Component {
  render() {
    if (this.props.data.isLoading) {
      return (
        <div> 
          <p> 
            Loading...
          </p>
        </div>
      );
    }

    if (!this.props.data.itemData) {
      return (
        <div> 
          <p> 
            Take a photo with the item to make a purchase.
          </p>
        </div>
      );
    }

    return (
      <div>
        <p> Thanks for purchasing {this.props.data.itemData.name} for {this.props.data.itemData.price} </p>
      </div>
    );
  }
}

export default Item;
