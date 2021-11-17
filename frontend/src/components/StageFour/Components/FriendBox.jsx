import globalStyles from "../../../styles/styles.module.css";


const FriendBox = (props) => {
  return (
    <div className={globalStyles.wrapper}>
      <div className={globalStyles.friendInfoHeader}>
        <span> 
          <img className={globalStyles.profilePicture} src={props.friend.profilePictureURL}/> 
        </span>
        <span>
          <span className={globalStyles.friendName}>{props.friend.name}</span>
          <span className={globalStyles.friendH4}>{props.friend.mutualFriendCount} Mutual Friends</span>
        </span>
      </div>

      <div className={globalStyles.friendInfo}>
          <h3 className={globalStyles.about}> About </h3>

          <div className={`${globalStyles.itemBoxes} ${globalStyles.bigBox}`}>
            <h3 className={globalStyles.topRow}>Workplace</h3>
              {props.friend.workplace.map( (entry) =>
                  <h5 className={globalStyles.knownInfo}>{entry}</h5>
              )}
            <h3>College</h3>
              {props.friend.college.map( (entry) =>
                  <h5 className={globalStyles.knownInfo}>{entry}</h5>
              )}
            <h3>High School</h3>
              {props.friend.highschool.map( (entry) =>
                  <h5 className={globalStyles.knownInfo}>{entry}</h5>
              )}
            <h3>Places Lived</h3>
              {props.friend.places.map( (entry) =>
                  <h5 className={globalStyles.knownInfo}>{entry}</h5>
              )}
            <h3>Religious Views</h3>
              {props.friend.religion.map( (entry) =>
                  <h5 className={globalStyles.knownInfo}>{entry}</h5>
              )}
            <h3>Political Views</h3>
              {props.friend.politics.map( (entry) =>
                  <h5 className={globalStyles.knownInfo}>{entry}</h5>
              )}
          </div>
      </div>
    </div>
  );
};

export default FriendBox;
