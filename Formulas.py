# 2.1 No. of Rains


=LET(
  rawA; A:A;
  rawB; B:B;
  
  results; MAP(SEQUENCE(ROWS(rawA)); LAMBDA(i;
    LET(
      dateStr; TO_TEXT(INDEX(rawA; i));
      isDate; ISNUMBER(SEARCH("/"); dateStr));
      
      IF(NOT(isDate); 0;
        LET(
          currB; TRIM(TO_TEXT(INDEX(rawB; i)));
          IF(currB <> ""; 1;
            IF(i = 1; 1;
              LET(
                prevB; TRIM(TO_TEXT(INDEX(rawB; i - 1)));
                startHr; IFERROR(VALUE(REGEXEXTRACT(prevB; "^[^0-9]*(\d{1,2})")); -1);
                endHr; IFERROR(VALUE(REGEXEXTRACT(prevB; "-\s*[^0-9]*(\d{1,2})")); 99);
                
                IF(AND(prevB <> ""; startHr > -1; endHr < 99; endHr < startHr); 0; 1)
              )
            )
          )
        )
      )
    )
  ));
  SUM(results)
)




# 2.2 Progress




=DATEDIF(DATE(2023; 6; 12); TODAY(); "Y") & " years, " & DATEDIF(DATE(2023; 6; 12); TODAY(); "YM") & " months, and " & DATEDIF(DATE(2023; 6; 12); TODAY(); "MD") & " days (" & DATEDIF(DATE(2023; 6; 12); TODAY(); "D") & " days)"




# 2.3 Code Gen




=IFERROR(IF(ISBLANK(INDIRECT(A1)); "#ERROR!"; 
  "#" & LET(
    targetRow; ROW(INDIRECT(A1));
    rawA; INDIRECT("A1:A" & targetRow);
    rawB; INDIRECT("B1:B" & targetRow);
    
    results; MAP(SEQUENCE(ROWS(rawA)); LAMBDA(i;
      LET(
        dateStr; TO_TEXT(INDEX(rawA; i));
        isDate; ISNUMBER(SEARCH("/"); dateStr));
        
        IF(NOT(isDate); 0;
          LET(
            currB; TRIM(TO_TEXT(INDEX(rawB; i)));
            IF(currB <> ""; 1;
              IF(i = 1; 1;
                LET(
                  prevB; TRIM(TO_TEXT(INDEX(rawB; i - 1)));
                  startHr; IFERROR(VALUE(REGEXEXTRACT(prevB; "^[^0-9]*(\d{1,2})")); -1);
                  endHr; IFERROR(VALUE(REGEXEXTRACT(prevB; "-\s*[^0-9]*(\d{1,2})")); 99);
                  
                  IF(AND(prevB <> ""; startHr > -1; endHr < 99; endHr < startHr); 0; 1)
                )
              )
            )
          )
        )
      )
    ));
    SUM(results)
  )
); "#ERROR!")



# 2.4 Dura Gen



=IF(A1=""; "";
  LET(
    cleanInput; SUBSTITUTE(A1; " "; "");
    expandedStr; TEXTJOIN(","; TRUE;
      MAP(SPLIT(cleanInput; ","); LAMBDA(ref;
        IF(NOT(REGEXMATCH(ref; ":")); ref;
          LET(
            colStr; REGEXEXTRACT(ref; "^[A-Za-z]+");
            leftPart; REGEXEXTRACT(ref; "^[^:]+");
            rightPart; REGEXEXTRACT(ref; ":.+$");
            rStart; VALUE(REGEXEXTRACT(leftPart; "\d+"));
            rEnd; VALUE(REGEXEXTRACT(rightPart; "\d+"));
            TEXTJOIN(","; TRUE; MAP(SEQUENCE(rEnd - rStart + 1; 1; rStart); LAMBDA(r; colStr & r)))
          )
        )
      ))
    );
    
    IFERROR(
      JOIN(", ";
        MAP(SPLIT(expandedStr; ","); LAMBDA(cleanRef;
          LET(
            rawStr; TO_TEXT(INDIRECT(cleanRef));
            
            timeStr; IF(rawStr <> ""; rawStr;
              LET(
                colStr; REGEXEXTRACT(cleanRef; "^[A-Za-z]+");
                tRow; VALUE(REGEXEXTRACT(cleanRef; "\d+$"));
                lastFilled; IF(tRow <= 1; ""; 
                  IFERROR(
                    LET(
                      prevRange; INDIRECT(colStr & "1:" & colStr & (tRow - 1));
                      filtered; FILTER(prevRange; prevRange <> "");
                      INDEX(filtered; ROWS(filtered))
                    ); 
                    ""
                  )
                );
                
                startHr; IFERROR(VALUE(REGEXEXTRACT(lastFilled; "^[^0-9]*(\d{1,2})")); -1);
                endHr; IFERROR(VALUE(REGEXEXTRACT(lastFilled; "-\s*[^0-9]*(\d{1,2})")); 99);
                
                IF(AND(lastFilled <> ""; startHr > -1; endHr < 99; endHr < startHr); lastFilled; "")
              )
            );
            
            startMatch; IFERROR(REGEXEXTRACT(timeStr; "(\d{1,2}:\d{2})"); "");
            endMatch; IFERROR(REGEXEXTRACT(timeStr; "-.*?(\d{1,2}:\d{2})"); "");
            hasTilde; REGEXMATCH(timeStr; "~");
            
            IF(OR(startMatch=""; endMatch=""); "#INCOMPLETE!";
              LET(
                startVal; TIMEVALUE(startMatch);
                endVal; TIMEVALUE(endMatch);
                exactMins; ROUND(MOD(endVal - startVal; 1) * 24 * 60; 0);
                finalMins; IF(AND(hasTilde; exactMins >= 5); MROUND(exactMins; 5); exactMins);
                h; INT(finalMins / 60);
                m; MOD(finalMins; 60);
                IF(h>0; h & "h" & IF(m>0; m & "m"; ""); m & "m")
              )
            )
          )
        ))
      );
      "#INCOMPLETE!"
    )
  )
)



# 2.5 Debug: Incorrect and Incomplete



=LET(
  ignoreBox; REGEXREPLACE(TO_TEXT(A1); "(?i)^Ignore:\s*"; "");
  results; MAP(List!B:B; SEQUENCE(ROWS(List!B:B); 1; 1); LAMBDA(val; r;
    LET(
      timeStr; TO_TEXT(val);
      addr; "B" & r;
      isIgnored; IFERROR(REGEXMATCH(ignoreBox; "(?i)\b" & addr & "\b"); FALSE);
      
      IF(OR(NOT(REGEXMATCH(timeStr; ":")); isIgnored); "";
        LET(
          hasPipe; REGEXMATCH(timeStr; "\|");
          timePart; IF(hasPipe; REGEXEXTRACT(timeStr; "^([^|]+)"); timeStr);
          manualPartRaw; IF(hasPipe; REGEXEXTRACT(timeStr; "\|(.*)$"); "");
          manualPart; TRIM(SUBSTITUTE(manualPartRaw; "~"; ""));
          startMatch; IFERROR(REGEXEXTRACT(timePart; "(\d{1,2}:\d{2})"); "");
          endMatch; IFERROR(REGEXEXTRACT(timePart; "-.*?(\d{1,2}:\d{2})"); "");
          hasTilde; REGEXMATCH(timePart; "~");
          
          isComp; AND(hasPipe; manualPart <> ""; startMatch <> ""; endMatch <> "");
          
          IF(NOT(isComp);
            "Incomplete|" & addr;
            LET(
              startVal; TIMEVALUE(startMatch);
              endVal; TIMEVALUE(endMatch);
              exactMins; ROUND(MOD(endVal - startVal; 1) * 24 * 60; 0);
              finalMins; IF(AND(hasTilde; exactMins >= 5); MROUND(exactMins; 5); exactMins);
              h; INT(finalMins / 60);
              m; MOD(finalMins; 60);
              calcDuration; IF(h>0; h & "h" & IF(m>0; m & "m"; ""); m & "m");
              
              isSecondOverride; AND(exactMins <= 1; REGEXMATCH(manualPart; "(?i)[05]s$"));
              
              IF(OR(calcDuration = manualPart; isSecondOverride); ""; "Incorrect|" & addr)
            )
          )
        )
      )
    )
  ));
  
  incArr; MAP(results; LAMBDA(x; IF(LEFT(x; 10)="Incomplete"; MID(x; 12; 100); "")));
  wrongArr; MAP(results; LAMBDA(x; IF(LEFT(x; 9)="Incorrect"; MID(x; 11; 100); "")));
  
  incJoin; TEXTJOIN(", "; TRUE; incArr);
  wrongJoin; TEXTJOIN(", "; TRUE; wrongArr);
  
  incText; IF(incJoin=""; "Incomplete: false"; "Incomplete: " & incJoin);
  wrongText; IF(wrongJoin=""; "Incorrect: false"; "Incorrect: " & wrongJoin);
  
  TEXTJOIN(CHAR(10); TRUE; incText; wrongText)
)


# 2.6 Debug: Date Spikes Check



=LET(
  ignoreBox; TO_TEXT(A5);
  rawRange; List!A5:A;
  
  rawDates; MAP(rawRange; LAMBDA(cell;
    LET(
      num; N(cell);
      parsed; IFERROR(DATEVALUE(TO_TEXT(cell)); 0);
      val; IF(num > 40000; num; parsed);
      IF(val > 40000; val; 0)
    )
  ));
  
  idxList; FILTER(SEQUENCE(ROWS(rawDates)); rawDates > 0);
  validDates; FILTER(rawDates; rawDates > 0);
  totalValid; ROWS(idxList);
  
  revDates; MAP(SEQUENCE(totalValid; 1; totalValid; -1); LAMBDA(idx; INDEX(validDates; idx)));
  revMins; SCAN(9999999; revDates; LAMBDA(acc; v; MIN(acc; v)));
  runningMins; MAP(SEQUENCE(totalValid); LAMBDA(idx; INDEX(revMins; totalValid - idx + 1)));
  
  results; MAP(SEQUENCE(totalValid); LAMBDA(i;
    LET(
      currIdx; INDEX(idxList; i);
      currDate; INDEX(validDates; i);
      addr; "A" & (currIdx + 4);
      dateStr; TEXT(currDate; "dd/MM/yyyy");
      
      isIgnored; IFERROR(REGEXMATCH(ignoreBox; "(?i)\b" & addr & "\b"); FALSE);
      
      IF(isIgnored; "";
        IF(currDate > TODAY();
          dateStr & " - " & addr ;
          IF(i < totalValid;
            IF(currDate > INDEX(runningMins; i + 1);
              dateStr & " - " & addr ;
              ""
            );
            ""
          )
        )
      )
    )
  ));
  
  errors; FILTER(results; results <> "");
  IFERROR("NoError: false (" & TEXTJOIN(", "; TRUE; errors) & ")"; "NoError: true :)")
)
