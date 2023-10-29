import React from "react";

export interface AnswerProps {
  answer_plain_text: string;
  answer_original: string;
  notes: string;
}

const Answer: React.FC<AnswerProps> = ({
  answer_plain_text,
  answer_original,
  notes,
}) => {
  const items = answer_plain_text
    .split(/\d\./)
    .filter((item) => item.trim() !== "");

  return (
    <div>
      <p>
        <strong>Answer plain text: </strong>
        {items.map((item, index) => (
          <li key={index}>{item.trim()}</li>
        ))}
      </p>

      <p>
        <strong>Answer original: </strong>
        <div dangerouslySetInnerHTML={{ __html: answer_original }} />
      </p>
      <p>
        <strong>Notes: </strong>
        {notes}
      </p>
    </div>
  );
};

export default Answer;
