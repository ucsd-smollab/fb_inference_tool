import styles from "../StageThreeStepThree.module.css"

const ColumnData = (props) => {
  const data = props.data;
  return (
    <div>
      {data && data.map( (entry) =>
        <h2 style={{"lineHeight": "0.8"}}>{entry}</h2>
      )}
    </div>
  );
};

export default ColumnData;
