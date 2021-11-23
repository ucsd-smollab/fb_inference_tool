import { useEffect, useState } from "react";

import FriendBox from "./Components/FriendBox";

import globalStyles from "../../styles/styles.module.css";
import mainStyles from "./StageFour.modules.css";

const StageFour = (props) => {
  const [query, changeQuery] = useState("");
  const [friendData, changeFriendData] = useState([]);
  const exampleFriendData = {
    name: 'Jacey Smith',
    mutualFriendCount: '321',
    profilePictureURL: 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcREQSG0xK1r5xe4WvQsV7WTNey9OSBunMh6GLY8HcxYUinuG_hHJ4IWUtjeAcV3M7bfhbo&usqp=CAU',
    workplace: ['UCSD Department of Computer Science'],
    college: ['University of California San Diego'],
    highschool: ['No Data'],
    places: ['Los Angeles', 'San Diego'],
    religion: ['No Data'],
    politics: ['No Data']
  };

  useEffect(() => {
    changeFriendData(["gello", "hello", "wow"]);
  }, []);

  return (
    <div className={globalStyles.background}>
    <div className={globalStyles.SearchContainer}>
      <div className={globalStyles.SearchBar}>
        <input type="text" placeholder="" onChange={event => changeQuery(event.target.value)} />
      </div>
    </div>
    <FriendBox friend={exampleFriendData}/>
    </div>
  );
};

export default StageFour;
