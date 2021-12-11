import { useEffect, useState } from "react";

import FriendBox from "./Components/FriendBox";
import Dropdown from "./Components/Dropdown";

import globalStyles from "../../styles/styles.module.css";
import mainStyles from "./StageFour.modules.css";

const StageFour = (props) => {
  const emptyFriendData = {
    shared: {
      name: '',
      mutualFriendCount: '',
      profilePictureURL: '',
      workplace: [''],
      college: [''],
      highschool: [''],
      places: [''],
      religion: [''],
      politics: ['']
    },
    inferred: {
      work_inf: '',
      college_inf: '',
      hs_inf: '',
      places_inf: '',
      religion_inf: '',
      politic_inf: ''
    }
  };

  const [query, changeQuery] = useState("Type Name Here");
  const [selectedFriend, changeSelectedFriend] = useState("");
  const [friendData, changeFriendData] = useState(emptyFriendData);
  const [searchFriendSuggestions, changeSearchFriendSuggestions] = useState([]);

  useEffect(() => {
    const url = "http://localhost:5000/stage_four_friend?friend_url=" + encodeURIComponent(selectedFriend);
    const getFriendData = fetch(url, {
      method: "GET",
      headers: { "Content-Type": "application/json" },
    }).then(res => res.json()).then(data => {
      changeFriendData(data)
    });
  }, [selectedFriend]);

  useEffect(() => {
      const url = "http://localhost:5000/stage_four_query?query=" + encodeURIComponent(query);
      const getFriendQuery= fetch(url, {
        method: "GET",
        headers: { "Content-Type": "application/json" },
      }).then(res => res.json()).then(data => {
        changeSearchFriendSuggestions(data)
      });
  }, [query]);

  function handleChange(newValue) {
    changeQuery(newValue);
  }

  const onClickChangeSelected = (newUrl) => {
    changeSelectedFriend(newUrl)
  }

  return (
    <div className={globalStyles.background}>
    <Dropdown onChange={handleChange} friendSuggestions={searchFriendSuggestions} onClick={onClickChangeSelected}/>
    <FriendBox friend={friendData}/>
    </div>
  );
};

export default StageFour;
