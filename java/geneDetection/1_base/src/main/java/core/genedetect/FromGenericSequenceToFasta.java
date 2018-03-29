/*
 *  Copyright 2002-2015 Barcelona Supercomputing Center (www.bsc.es)
 *
 *  Licensed under the Apache License, Version 2.0 (the "License");
 *  you may not use this file except in compliance with the License.
 *  You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 *  Unless required by applicable law or agreed to in writing, software
 *  distributed under the License is distributed on an "AS IS" BASIS,
 *  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 *  See the License for the specific language governing permissions and
 *  limitations under the License.
 */

package core.genedetect;

import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlType;


/**
 * <p>Java class for fromGenericSequenceToFasta complex type.
 * 
 * <p>The following schema fragment specifies the expected content contained within this class.
 * 
 * <pre>
 * &lt;complexType name="fromGenericSequenceToFasta">
 *   &lt;complexContent>
 *     &lt;restriction base="{http://www.w3.org/2001/XMLSchema}anyType">
 *       &lt;sequence>
 *         &lt;element name="seqId" type="{http://genedetect.core}NemusObject" minOccurs="0"/>
 *       &lt;/sequence>
 *     &lt;/restriction>
 *   &lt;/complexContent>
 * &lt;/complexType>
 * </pre>
 * 
 * 
 */
@XmlAccessorType(XmlAccessType.FIELD)
@XmlType(name = "fromGenericSequenceToFasta", propOrder = {
    "seqId"
})
public class FromGenericSequenceToFasta {

    protected NemusObject seqId;

    /**
     * Gets the value of the seqId property.
     * 
     * @return
     *     possible object is
     *     {@link NemusObject }
     *     
     */
    public NemusObject getSeqId() {
        return seqId;
    }

    /**
     * Sets the value of the seqId property.
     * 
     * @param value
     *     allowed object is
     *     {@link NemusObject }
     *     
     */
    public void setSeqId(NemusObject value) {
        this.seqId = value;
    }

}